import unittest

from pyklout import Klout, KloutError


class TestKlout(unittest.TestCase):

    KEY = 'ADD YOUR KLOUT API KEY HERE.'

    def test_createKloutAPI(self):
        api = Klout(self.KEY)
        self.assertEquals(api._api_key, self.KEY)

    def test_scores(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.score(['rafaelcaricio'])
        self.assertEquals(data[0][0], 'rafaelcaricio')
        self.assert_(data[0][1] < 100.0  and data[0][1] > 0.0)

        #Valid Test 5 usernames
        api = Klout(self.KEY)
        data = api.score(['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google'])
        for (key, value) in data:
            self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google'])
            self.assert_(value <= 100.0  and value >= 0.0)

        #Valid Test Invalid Username in Twitter
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.score, ['ahahahahah'])

        #Valid Test No Data
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.score, [])

        #Valid Test More than 5
        api = Klout(self.KEY)
        usernames = ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google', 'timoreilly','googleapps']
        data = api.score(usernames)
        self.assertEquals(len(data),5)
        for (key, value) in data:
            self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google'])
            self.assert_(value <= 100.0  and value >= 0.0)

    def test_users_show(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.users_show(['rafaelcaricio'])
        self.assertEquals(len(data),1)
        self.assertEquals(data[0]['twitter_screen_name'],'rafaelcaricio')
        for user in data:
            for key in user.keys():
                self.assert_(key in ['score', 'twitter_id', 'twitter_screen_name'])

        #Valid Test 5 usernames
        api = Klout(self.KEY)
        data = api.users_show(['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])
        self.assertEquals(len(data),5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['score', 'twitter_id', 'twitter_screen_name'])

        #Valid Test Invalid Username in Twitter
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_show, ['ahahahahah'])

        #Valid Test No Data
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_show, [])

        #Valid Test More than 5
        api = Klout(self.KEY)
        usernames = ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'pugpe', 'srlm']
        data = api.users_show(usernames)
        self.assertEquals(len(data),5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['score', 'twitter_id', 'twitter_screen_name'])

    def test_users_topics(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.users_topics(['marcelcaraciolo'])
        self.assertEquals(len(data),1)
        self.assertEquals(data[0].keys(),['marcelcaraciolo'])

        #Valid Test 5 usernames
        api = Klout(self.KEY)
        data = api.users_topics(['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])
        self.assert_(len(data) <= 5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])

        #Valid Test Invalid Username in Twitter
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_topics, ['ahahahahah'])

        #Valid Test No Data
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_topics, [])

        #Valid Test More than 5
        api = Klout(self.KEY)
        usernames = ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google', 'timoreilly','googleapps']
        data = api.users_topics(usernames)
        self.assert_(len(data) <= 5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google'])

    def test_users_influenced_by(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.users_influenced_by(['marcelcaraciolo'])
        self.assertEquals(len(data),1)
        self.assertEquals(data[0].keys(),['marcelcaraciolo'])

        #Valid Test 5 usernames
        api = Klout(self.KEY)
        data = api.users_influenced_by(['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])
        self.assert_(len(data) <= 5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])

        #Valid Test Invalid Username in Twitter
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_influenced_by, ['ahahahahah'])

        #Valid Test No Data
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_influenced_by, [])

        #Valid Test More than 5
        api = Klout(self.KEY)
        usernames = ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google', 'timoreilly','googleapps']
        data = api.users_influenced_by(usernames)
        self.assert_(len(data) <= 5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google'])

    def test_users_influencer_of(self):
        #Valid Test 1 username
        api = Klout(self.KEY)
        data = api.users_influencer_of(['marcelcaraciolo'])
        self.assertEquals(len(data),1)
        self.assertEquals(data[0].keys(),['marcelcaraciolo'])

        #Valid Test 5 usernames
        api = Klout(self.KEY)
        data = api.users_influencer_of(['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])
        self.assert_(len(data) <= 5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'srlm'])

        #Valid Test Invalid Username in Twitter
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_influencer_of, ['ahahahahah'])

        #Valid Test No Data
        api = Klout(self.KEY)
        self.assertRaises(KloutError, api.users_influencer_of, [])

        #Valid Test More than 5
        api = Klout(self.KEY)
        usernames = ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google', 'timoreilly','googleapps']
        data = api.users_influencer_of(usernames)
        self.assert_(len(data) <= 5)
        for user in data:
            for key in user.keys():
                self.assert_(key in ['rafaelcaricio', 'marcelcaraciolo', 'atepassar_', 'caocurseiro', 'google'])

unittest.main()
