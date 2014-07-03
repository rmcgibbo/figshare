import os
import six
import json
from requests_oauthlib import OAuth1Session

consumer_key = 'XJCbpn5nHHDNW48NBMx0eg'
consumer_secret = 'gcxv78Aq6kBulp663LFgug'


class Figshare(object):
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        """
        Connects to the figshare API.
        """
        self.client = OAuth1Session(
            consumer_key, consumer_secret, access_token, access_token_secret)
        self.endpoint = 'http://api.figshare.com/v1/my_data'

    def article(self, article_id):
        """
        Returns a single article.
        """
        response = self.client.get(self.endpoint + '/articles/%s' % article_id)
        return response.json()['items'][0]

    def delete_article(self, article_id):
        """
        Deletes article `article_id`.
        """
        response = self.client.delete(
            self.endpoint + '/articles/%s' % article_id)
        return json.loads(response.content)

    def articles(self, limit=None):
        """
        Parameters
        ----------

        limit : int or None
            If not None, then limit the number of articles returned.

        Returns
        -------
        Dict of {count: integer count of articles, items: dictionary
        representing each article}
        """
        # API only returns 10 results at a time, so keep asking for more pages
        # until we can't get any more...
        all_articles = []
        count = 0
        page = 1
        while True:
            if limit is not None and (len(all_articles) < limit):
                break
            data = {'page': page}
            response = self.client.get(
                self.endpoint + '/articles',
                params={'page': page}
            )
            # Keep the response around for debugging if needed; get a separate
            # results dict
            results = response.json()

            if results['count'] == 0:
                break

            all_articles.extend(results['items'])
            count += results['count']
            page += 1

        # Reconstruct the JSON dict in the same format returned by a single
        # response (with keys [count, items])
        assert count == len(all_articles)
        return {'count': count, 'items': all_articles}

    def create_article(self, title, description, defined_type='dataset'):
        """
        Create an article.

        `title`, `description` are required; other `defined_type` value can be
        "fileset".  There are likely others (e.g., "figure", "code", "media",
        etc) but these are currently undocumented by the API, so use at your
        own risk.
        """
        response = self.client.post(
            self.endpoint + '/articles',
            data=json.dumps({'title': title,
                             'description': description,
                             'defined_type': defined_type,
                             }),
            headers={'content-type': 'application/json'})
        return response.json()

    def make_private(self, article_id):
        """
        Make an article private.

        If an article was just created, it is still in draft form.  This method
        will turn it into a private article.
        """
        response = self.client.post(
            '%s/articles/%s/action/make_private' % (self.endpoint, article_id))
        return response.json()

    def update_article(self, article_id, title=None, description=None,
                       defined_type=None):
        """
        Update title, description, and defined_type.

        Any of these values can be None if you don't want to change them.
        """
        data = {'title': title,
                'description': description,
                'defined_type': defined_type}
        data = dict((k, v) for k, v in data.items() if v is not None)
        response = self.client.put(
            '%s/articles/%s' % (self.endpoint, article_id),
            data=json.dumps(data),
            headers={'content-type': 'application/json'})
        return response.json()

    def upload_file(self, article_id, filepath_or_buffer):
        """
        Upload a file.

        `filepath_or_buffer` can be a string or an open file object.
        """
        if isinstance(filepath_or_buffer, six.string_types):
            file = open(filepath_or_buffer, 'rb')
            own_handle = True
        else:
            file = filepath_or_buffer
            own_handle = False

        try:
            files = {'filedata': (os.path.basename(file.name), file)}
            response = self.client.put(
                '%s/articles/%s/files' % (self.endpoint, article_id),
                files=files)
            return response.json()
        finally:
            if own_handle:
                file.close()

    def delete_file(self, article_id, file_id):
        """
        Delete a file.
        """
        response = self.client.delete(
            '%s/articles/%s/files/%s' % (self.endpoint, article_id, file_id)
        )
        return response.json()

    def add_link(self, article_id, link):
        """
        Add a link.
        """
        response = self.client.put(
            self.endpoint + '/articles/%s/links' % article_id,
            data=json.dumps({'link': link}),
            headers={'content-type': 'application/json'}
        )
        return response.json()

    def delete_link(self, article_id, link_id):
        """
        Delete a link.

        This requires a link ID, which you can get from inspecting the article
        JSON.  For example::

            first_link_id = article['links'][0]['id']
        """
        response = self.client.delete(
            self.endpoint + '/articles/%s/links/%s' % (article_id, link_id)
        )
        return reponse.json()

    def versions(self, article_id):
        """
        Show the versions of this article
        """
        response = self.client.get(
            self.endpoint + '/articles/%s/versions' % article_id
        )
        return response.json()

    def get_version(self, article_id, version_number):
        """
        Get a particular version of this article.
        """
        response = self.client.get(
            self.endpoint + '/articles/%s/versions/%s' % (article_id, version_number)
        )
        return response.json()

    def categories(self):
        """
        Show the possible categories supplied by figshare.
        """
        response = self.client.get(
            self.endpoint.replace('/my_data', '') + '/categories'
        )
        return response.json()

    def add_tag(self, article_id, tag):
        """
        Add a tag to an article.
        """
        response = self.client.put(
            self.endpoint + '/articles/%s/tags' % article_id,
            data=json.dumps({'tag_name': tag}),
            headers={'content-type': 'application/json'})
        return response.json()

    def delete_tag(self, article_id, tag_id):
        """
        Delete a tag from an article.

        This requires a tag ID, which you can get from inspecting the article JSON.  For example::

            first_tag_id = article['tags'][0]['id']
        """
        response = self.client.delete(
            self.endpoint + '/articles/%s/categories/%s' % (article_id, tag_id)
        )
        return response.json()

    def add_category(self, article_id, category_id):
        """
        Add a category to an article.

        See the categories() method to see the options and to select
        a `category_id`.
        """
        response = self.client.put(
            self.endpoint + '/articles/%s/categories' % article_id,
            data=json.dumps({'category_id': category_id}),
            headers={'content-type': 'application/json'})
        return response.json()

    def delete_category(self, article_id, category_id):
        """
        Delete a category from an article.
        """
        response = self.client.delete(
            self.endpoint + '/articles/%s/categories/%s' %
            (article_id, category_id)
        )
        return response.json()

    def add_author(self, article_id, author_id):
        """
        Add an author to an article.
        """
        response = self.client.put(
            self.endpoint + '/articles/%s/categories' % article_id,
            data=json.dumps({'author_id': author_id}),
            headers={'content-type': 'application/json'})
        return response.json()

    def delete_author(self, article_id, author_id):
        """
        Delete an author from an article
        """
        response = self.client.delete(
            self.endpoint + '/articles/%s/categories/%s' %
            (article_id, author_id)
        )
        return response.json()
