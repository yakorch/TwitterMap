import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def getting_user_info(user_nickname: str):
    """
    Returns a dictionary with account info by user's nickname
    Args:
        user_nickname (str): user's nickname on Twitter without '@'
    Returns:
        a dictioanry with account's info
    """
    if (len(user_nickname) < 1): 
        return None
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': user_nickname})
    # print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    return json.loads(data)
    # headers = dict(connection.getheaders())
    # print('Remaining', headers['x-rate-limit-remaining'])
