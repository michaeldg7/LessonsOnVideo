import json
import urllib
import urllib2


def get_facebook_shares(link=None):
    """
    Sends request to Facebook's Graph API and returns number of SHARES
    """
    shares = 0
    if link:
        facebook_api = "https://api.facebook.com/method/links.getStats?urls=%s&format=json" % (link, )
        url = urllib2.urlopen(facebook_api).read()
        content = json.loads(url)
        shares = content[0]['share_count']
    return shares


def get_twitter_tweets(link=None):
    """
    Sends request to Twitter API and returns number of TWEETS
    """
    tweets = 0
    if link:
        twitter_api = "http://urls.api.twitter.com/1/urls/count.json?url=%s" % (link, )
        url = urllib2.urlopen(twitter_api).read()
        content = json.loads(url)
        tweets = content['count']
    return tweets


def get_google_count(link=None):
    """
    Sends request to Google Plus API and returns number of SHARES
    """
    count = 0
    if link:
        target = urllib.quote_plus(link+"#__sid=0") #url-friendly
        data = 'f.req=%5B%22'+target+'%22%2Cnull%5D&'
        url = "https://plus.google.com/u/0/ripple/update"
        req = urllib2.Request(url, data, {'Content-Type': 'application/x-www-form-urlencoded'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        response = response[6:] #remove some bad characters
        response_json_str = response.replace(",,", ",null,").replace(",,", ",null,")
        datas = json.loads(response_json_str)
         
        # Find relevant data -- might need to be changed depending on possible incoming format
        # Maybe need some recursive func searching for list with first item "orr.c"
        count = datas[0][1][-3]
    
    return count


def get_shares(link):
    shares = {
        "facebook": get_facebook_shares(link),
        "twitter": get_twitter_tweets(link),
        "google_plus": get_google_count(link),
    }
    return shares