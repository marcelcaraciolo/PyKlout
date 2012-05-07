# -*- coding: utf-8 -*-


"""
A Python interface for the Klout API.

Use of PyKlout requires a Klout API key.
You can register and get a key at

    <http://http://klout.com/s/developers/v2>


https://github.com/marcelcaraciolo/PyKlout


"""


__author__ = 'Marcel Caraciolo'
__version__ = '0.2'


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

        return data
    
    def identity(self, network_id, network='tw'):
        """
        This method allows you to retrieve the user identity.

        Parameters
        ----------
        network: From which network you want to retrieve the score object.
                 By default the value is tw (twitter).
        networkId: The network id generally represented by the numerical id.

        Returns
        -------
        A JSON dict containing the klout id in the format:
        {u'id': u'709406', u'network': u'ks'}

        """

        url = '/v2/identity.json/%s'
        
        if not network_id or network not in ['tw', 'ks','twitter']:
            raise KloutError(0, 'Insufficient parameters')

        if isinstance(network_id, str):
            query = {'screenName': network_id}
            url = url % 'twitter'
        else:
            query = {}
            url = url % network 
            url += '/%d' % network_id

        data = self.make_api_call(url, query)
        
        return data

    def score(self, id):
        """
        This method allows you to retrieve the user score.

        Parameters
        ----------
        id :  the numerical id (klout id)
    
        Returns
        ---------
        The dict containing the user id and klout score and score deltain the format:
        {u'score': 51.613044738769531, u'scoreDelta': {u'dayChange': -0.25563812255859375,
         u'monthChange': -0.54084014892578125, u'weekChange': -0.67768478393554688}}
        """

        url = '/v2/user.json/%s/%s'
        
        if not id:
            raise KloutError(0, 'Insufficient parameters')

        query = {}
        url = url % (id, 'score')

        data = self.make_api_call(url, query)
        
        return data
        
    def influences(self, id):
        """
        This method allows you to retrieve the influences by and of the user.

        Parameters
        ----------
        id :  the numerical id (klout id)
    
        Returns
        ---------
        Influence returns two arrays:
        myInfluencers - Who influences the user
        myInfluencees - Whom the user influences
        """
        url = '/v2/user.json/%s/%s'

        if not id:
            raise KloutError(0, 'Insufficient parameters')

        query = {}
        url = url % (id, 'influence')

        data = self.make_api_call(url, query)

        return data


    def topics(self, id):
        """
        This method allows you to retrieve the topics a user is influential in..

        Parameters
        ----------
        id :  the numerical id (klout id)

        Returns
        ---------
		Topics returns a limited array of topics, with important metadata:
		
		id - The unique id for the Klout Topic
		displayName - A friendly name for the topic
		name - A less-friendly name for the topic
		slug - A helper to build a URL for the topic: http://klout.com/#/topic/{slug}
		imageUrl - URL to Klout's image for the topic
		
		"""
        url = '/v2/user.json/%s/%s'

        if not id:
            raise KloutError(0, 'Insufficient parameters')

        query = {}
        url = url % (id, 'topics')

        data = self.make_api_call(url, query)

        return data
