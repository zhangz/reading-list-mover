import sys
import json
import urllib
import urllib2
import urlparse
import json as simplejson
from xml.dom.minidom import parseString
import xml.dom.minidom
import oauth2
import ConfigParser
from StringIO import StringIO
import gzip

class OAuthClient:
    def __init__(self, key, secret, user, password):
        consumer = oauth2.Consumer(key, secret)
        client = oauth2.Client(consumer)
        resp, content = client.request(self.token_url, "POST", urllib.urlencode({
            'x_auth_mode': 'client_auth',
            'x_auth_username': user,
            'x_auth_password': password
        }))
        token = dict(urlparse.parse_qsl(content))
        token = oauth2.Token(token['oauth_token'], token['oauth_token_secret'])
        self.http = oauth2.Client(consumer, token)
        
    def getBookmarks(self):
        response, data = self.http.request(self.get_url, method='GET') 
        bookmarks = []
        
        for b in simplejson.loads(data)['bookmarks']:
            article = b['article']
            bookmarks.append({'url' : article['url'], 'title' : article['title']})
            
        return bookmarks
        
    def addBookmark(self, bookmark):
        self.http.request(self.add_url, method='POST', body=urllib.urlencode({
            'url': bookmark['url'],
            'title': bookmark['title'].encode('utf-8')
        })) 

class Readability(OAuthClient):
    def __init__(self, key, secret, user, password):
        self.token_url = 'https://www.readability.com/api/rest/v1/oauth/access_token/'
        self.get_url   = 'https://www.readability.com/api/rest/v1/bookmarks'
        self.add_url   = 'https://www.readability.com/api/rest/v1/bookmarks'
        
        OAuthClient.__init__(self, key, secret, user, password)
        
class Instapaper(OAuthClient):
    def __init__(self, key, secret, user, password):
        self.token_url = 'https://www.instapaper.com/api/1/oauth/access_token'
        self.get_url   = 'https://www.instapaper.com/api/1/bookmarks/list'
        self.add_url   = 'https://www.instapaper.com/api/1/bookmarks/add'
        
        OAuthClient.__init__(self, key, secret, user, password)
        
    def getBookmarks(self):
        '''
        The ability to export bookmarks from Instapaper is reserved for users with Subscription accounts, if you have
        such an account and wish to enable this feature just delete this function
        '''
        raise Exception('Not supported')

class HttpAuthClient:
    def __init__(self, user, password):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, self.get_url, user, password)
        passman.add_password(None, self.add_url, user, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        self.url_opener = urllib2.build_opener(authhandler)

    def open(self, url, data=None):
        return self.url_opener.open(url, data)
        
class Pocket:
    def __init__(self, key, token):
        base_args=urllib.urlencode({'consumer_key' : key, 'access_token' : token, 'sort' : 'oldest'})
        self.get_url = 'https://getpocket.com/v3/get?' + base_args + '&'
        self.add_url = 'https://getpocket.com/v3/add?' + base_args + '&' 

    def getBookmarks(self):
        get_args=urllib.urlencode({'state' : 'unread'})
        data = json.load(urllib2.urlopen(self.get_url + get_args))
        return [{'url' : b['given_url'], 'title' : b['given_title']} for b in data['list'].values()]
        
    def addBookmark(self, bookmark):
        add_args=urllib.urlencode({'url' : bookmark['url']})
        urllib2.urlopen(self.add_url + add_args)

config = ConfigParser.RawConfigParser()
config.read('config.txt')

def buildReadability():
    SECTION = 'Readability'
    return Readability(config.get(SECTION, 'key'), config.get(SECTION, 'secret'), config.get(SECTION, 'user'), config.get(SECTION, 'password'))

def buildPocket():
    SECTION = 'Pocket'
    return Pocket(config.get(SECTION, 'key'), config.get(SECTION, 'token'))

def buildInstapaper():
    SECTION = 'Instapaper'
    return Instapaper(config.get(SECTION, 'key'), config.get(SECTION, 'secret'), config.get(SECTION, 'user'), config.get(SECTION, 'password'))


