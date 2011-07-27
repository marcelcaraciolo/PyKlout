# -*- coding: utf-8 -*-


"""
A Python interface for the Klout API.

Use of PyKlout requires a Klout API key.
You can register and get a key at

    <http://developer.klout.com/member/register>


https://github.com/marcelcaraciolo/PyKlout


"""


__author__ = 'Marcel Caraciolo'
__version__ = '0.1'


import urllib
import httplib
import json
import urllib2

ERROR_STATUS = {
    # "200: "OK: Success", IS A GOOD STATUS
    202: "Accepted: Your request was accepted and the user was queued for processing.",
    401: "Not Authorized: either you need to provide authentication credentials, or the credentials provided aren't valid.",
    403: "Bad Request: your request is invalid, This is the status code returned if you've exceeded the rate limit or if you are over QPS.",
    404: "Not Found: either you're requesting an invalid URI or the resource in question doesn't exist (ex: no such user in our system).",
    500: "Internal Server Error: we did something wrong.",
    502: "Bad Gateway: returned if Klout is down or being upgraded.",
    503: "Service Unavailable: the Klout servers are up, but are overloaded with requests. Try again later.",
}


class KloutError(Exception):
    def __init__(self, code, msg):
        super(KloutError, self).__init__()
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '%i: %s' % (self.code, self.msg)


class Klout(object):
    '''
    Klout API Handler

    Parameters
    ----------
    api_key : string the Klout API Key.

    '''
    API_URL = 'api.klout.com'

    def __init__(self, api_key):
        self._api_key = api_key

    def _remove_empty_params(self, params):
        '''
        Remove all unused parameters

        Parameters
        ----------
        params:  dict object
            A set of parameters key,value

        Returns
        --------
        The set of parameters as dict without empty parameters
        '''
        ret = {}
        for key in params:
            if not params[key] == None:
                ret[key] = params[key]

        return ret

    def make_api_call(self, url, query={}, body={}):
        '''
        Make the API Call to Klout

        Parameters
        ----------
        url: the url to call
        query: The GET parameters
        body: The POST parameters
        '''

        query = self._remove_empty_params(query)

        if 'key' not in query:
            query['key'] = self._api_key

        body = self._remove_empty_params(body)
        query_str = urllib.urlencode(query)
        body_str = urllib.urlencode(body)

        if len(query) > 0:
            if url.find('?') == -1:
                url = url + '?' + query_str
            else:
                url = url + '&' + query_str

        try:
            conn = httplib.HTTPConnection(self.API_URL)
            if body_str:
                conn.request('POST', url, body_str)
            else:
                conn.request('GET', url)
            resp = conn.getresponse()
            data = resp.read()
            data = json.loads(data)
        except httplib.HTTPException as err:
            msg = err.read() or ERROR_STATUS.get(err.code, err.message)
            raise KloutError(err.code, msg)
        except ValueError:
            msg = 'Invalida data: %s' % data
            raise KloutError(0, msg)
        else:
            status = data.pop("status")
            if status in ERROR_STATUS:
                msg = ERROR_STATUS.get(status, "Unknow Error")
                raise  KloutError(status, msg)

        if data.get('body', None):
            status = data.pop("status")
            msg = data['body']['error']
            raise  KloutError(status, msg)

        return data

    def score(self, users):
        """
        This method allows you to retrieve a Klout score

        Parameters
        ----------
        users: The usernames from whom fetching the scores

        Returns
        -------
        A list of tuples in the form [('user1', score1), ('user2', score2)...]
        Names are returned as unicode strings and scores as floats

        """
        url = '/1/klout.json'

        if not users:
            raise KloutError(0, 'No Users')

        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        query = {'users': users}

        data = self.make_api_call(url, query)

        return  [(r['twitter_screen_name'], r['kscore']) for r in data['users']]

    def users_show(self, users):
        """
        This method allows you to retrieve the user objects

        Parameters
        ----------
        users: The usernames from whom fetching the scores

        Returns
        -------
        A dictionary with the returned data.

        """
        url = '/1/users/show.json'

        if not users:
            raise KloutError(0, 'No Users')

        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        query = {'users': users}

        data = self.make_api_call(url, query)

        return  data['users']

    def users_topics(self, users):
        """
        This method allows you to retrieve the top 3 topic objects

        Parameters
        ----------
        users: The usernames from whom fetching the top topics

        Returns
        -------
        A list of dicts in the form [{'username':['topic1', 'topic2', ..]}]
        usernames and topics are returned as unicode strings

        """
        url = '/1/users/topics.json'

        if not users:
            raise KloutError(0, 'No Users')

        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        query = {'users': users}

        data = self.make_api_call(url, query)

        data = data['users']

        return [{user['twitter_screen_name']:[topic  for topic in user['topics']]} for user in data]

    def users_influenced_by(self, users):
        """
        This method allows you to retrieve up to 5 user score pairs
            for users that are influenced by the given influencer

        Parameters
        ----------
        users: The usernames from it will fetch the influenced usernames

        Returns
        -------
        A list of dicts in the form [{'username':[('username',kscore), ('username2','kscore2'),...]}]
        usernames are returned as unicode strings and kscores as floats.

        """
        url = '/1/soi/influenced_by.json'

        if not users:
            raise KloutError(0, 'No Users')

        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        query = {'users': users}

        data = self.make_api_call(url, query)

        data = data['users']

        return [{user['twitter_screen_name']:[(influencer['twitter_screen_name'], influencer['kscore']) \
            for influencer in user['influencers']]} for user in data]

    def users_influencer_of(self, users):
        """
        This method allows you to retrieve up to 5 user score pairs
            for users that are influencers of the given user.

        Parameters
        ----------
        users: The usernames from it will fetch the influenced usernames

        Returns
        -------
        A list of dicts in the form [{'username':[('username',kscore), ('username2','kscore2'),...]}]
        usernames are returned as unicode strings and kscores as floats.
        """
        url = self.API_URL + '/1/soi/influencer_of.json'

        if not users:
            raise KloutError(0, 'No Users')

        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        query = {'users': users}

        data = self.make_api_call(url, query)

        data = data['users']

        return [{user['twitter_screen_name']:[(influencer['twitter_screen_name'], influencer['kscore']) \
                for influencer in user['influencees']]} for user in data]