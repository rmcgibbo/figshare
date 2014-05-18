figshare command line client
============================
[![PyPI Version](https://badge.fury.io/py/figshare.png)](https://pypi.python.org/pypi/figshare)
[![Downloads](https://pypip.in/d/figshare/badge.png)](https://pypi.python.org/pypi/figshare)


This is a simple client for the figshare API in python.

Example
-------
```
$ figshare list_articles
Met-enkephalin MD Trajectories
------------------------------
article_id: 1026324
description: Ten ~50 ns molecular dynamics (MD) simulation
trajectories of the 5 residue Met-enkaphalin peptide. The aggregate
sampling is499.58 ns.Simulations were performed starting from the 1st...
	1plx.pdb			6 KB		file_id: 1497161
	trajectory_1.dcd			9.35 MB		file_id: 1497162
	trajectory_0.dcd			9.33 MB		file_id: 1497163
	trajectory_3.dcd			9.34 MB		file_id: 1497164
	trajectory_2.dcd			9.34 MB		file_id: 1497165
	trajectory_4.dcd			9.33 MB		file_id: 1497166
	trajectory_5.dcd			9.35 MB		file_id: 1497167
	trajectory_6.dcd			9.32 MB		file_id: 1497168
	trajectory_8.dcd			9.33 MB		file_id: 1497169
	trajectory_7.dcd			9.36 MB		file_id: 1497170
	trajectory_9.dcd			9.34 MB		file_id: 1497171
total size: 93.39 MB

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
No frills. `pip install figshare`. Or clone from github and `python setup.py install`.

Dependencies
------------
Just `requests_oauthlib`, and `six`. Get them with `pip install -r requirements.txt`
