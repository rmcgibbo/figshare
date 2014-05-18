figshare command line client
============================

This is a simple client for the figshare API in python.

Example
-------
```
$ figshare list_articles
{u'count': 1,
 u'filtered_by': u'permissions',
 u'items': [{u'article_id': 1030329,
 ...
 
$ figshare upload_file --article_id 1030329 --file /path/to/file
```

Install
-------

```
$ python setup.py install
```

Dependencies
------------
requests_oauthlib, six

```
pip install -r requirements.txt
```
