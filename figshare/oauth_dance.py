# This code was adapted from Python Twitter Tools (MIT license)
# https://github.com/sixohsix/twitter/blob/master/twitter/oauth_dance.py
# Authors: Mike Verdone, Robert T. McGibbon

from __future__ import print_function
import os
import time
import webbrowser
from requests_oauthlib import OAuth1Session

try:
    _input = raw_input
except NameError:
    _input = input


def write_token_file(filename, oauth_token, oauth_token_secret):
    """
    Write a token file to hold the oauth token and oauth token secret.
    """
    oauth_file = open(filename, 'w')
    print(oauth_token, file=oauth_file)
    print(oauth_token_secret, file=oauth_file)
    oauth_file.close()

def read_token_file(filename):
    """
    Read a token file and return the oauth token and oauth token secret.
    """
    with open(filename) as f:
        return f.readline().strip(), f.readline().strip()


def oauth_dance(app_name, consumer_key, consumer_secret, token_filename=None):
    """
    Perform the OAuth dance with some command-line prompts. Return the
    oauth_token and oauth_token_secret.

    Provide the name of your app in `app_name`, your consumer_key, and
    consumer_secret. This function will open a web browser to let the
    user allow your app to access their Twitter account. PIN
    authentication is used.

    If a token_filename is given, the oauth tokens will be written to
    the file.
    """
    print("Hi there! We're gonna get you all set up to use %s." % app_name)
    auth = OAuth1Session(consumer_key, consumer_secret)
    access_token = auth.fetch_access_token('http://api.figshare.com/v1/pbl/oauth/request_token')

    print("""
In the web browser window that opens please choose to Allow
access. Copy the PIN number that appears on the next page and paste or
type it here:
""")
    oauth_url = auth.authorization_url('http://api.figshare.com/v1/pbl/oauth/authorize')

    try:
        assert 'DISPLAY' in os.environ
        r = webbrowser.open(oauth_url)
        time.sleep(2) # Sometimes the last command can print some
                      # crap. Wait a bit so it doesn't mess up the next
                      # prompt.
        if not r:
            raise Exception()
    except:
        print("""
Uh, I couldn't open a browser on your computer. Please go here to get
your PIN:

""" + oauth_url)
    oauth_verifier = _input("Please enter the PIN: ").strip()
    access_token = auth.fetch_access_token('http://api.figshare.com/v1/pbl/oauth/access_token?oauth_verifier=%s' % oauth_verifier)
    oauth_token = access_token['oauth_token']
    oauth_token_secret = access_token['oauth_token_secret']

    if token_filename:
        write_token_file(
            token_filename, oauth_token, oauth_token_secret)
        print()
        print("That's it! Your authorization keys have been written to %s." % (
            token_filename))
    return oauth_token, oauth_token_secret
