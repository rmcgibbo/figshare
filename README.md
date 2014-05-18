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
 
$ figshare upload_file --article_id 1030329 --file ../1xd3/simulate_1xd3.py
{u'extension': u'py',
 u'id': 1502207,
 u'mime_type': u'text/x-python',
 u'name': u'simulate_1xd3.py',
 u'size': u'1 KB'}
 
$ figshare delete_file --article_id 1030329 --file_id 1502207
{u'success': u'Link to simulate_1xd3.py  deleted'}
```

Install
-------
No frills. Just `python setup.py install`

Dependencies
------------
Just `requests_oauthlib`, and `six`. Get them with `pip install -r requirements.txt`
