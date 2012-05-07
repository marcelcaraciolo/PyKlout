import unittest

from pyklout import Klout, KloutError


class TestKlout(unittest.TestCase):

    KEY = 'YOUR_API_KEY'

    def test_createKloutAPI(self):
        api = Klout(self.KEY)
        self.assertEquals(api._api_key, self.KEY)

    def test_identity(self):
        api = Klout(self.KEY)
        data = api.identity('marcelcaraciolo', 'twitter')
        self.assert_('id' in data)
        self.assert_('network' in data)

    def test_scores(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.identity('marcelcaraciolo', 'twitter')
        user_id = data['id']
        data = api.score(user_id)
        self.assert_(data['score'] < 100.0  and data['score'] > 0.0)
        
    def test_influences(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.identity('marcelcaraciolo', 'twitter')
        user_id = data['id']
        data = api.influences(user_id)
        self.assert_('myInfluencers' in data)
        self.assert_('myInfluencees' in data)

    def test_topics(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.identity('marcelcaraciolo', 'twitter')
        user_id = data['id']
        data = api.topics(user_id)
        for topic in data:
            for key in topic.keys():
                self.assert_(key in ['imageUrl','slug','displayName', 'id', 'name'])


unittest.main()
