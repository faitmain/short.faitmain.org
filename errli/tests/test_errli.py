import unittest

from pyramid import testing
from errli.views import new_url, get_url
from errli.db import SQLStorage


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include("cornice")
        self.config.scan("errli.views")
        self.config.registry['storage'] = SQLStorage('sqlite:///:memory:')

    def tearDown(self):
        testing.tearDown()

    def test_url(self):

        request = testing.DummyRequest()
        url = 'https://circus.readthedocs.org/en/latest/installation/'
        request.body = url

        result = new_url(request)
        key = result['short']
        self.assertEqual(key, 'installing-circus')

        request.body = ''
        request.matchdict['short_url'] = key
        res = get_url(request)
        self.assertEqual(res.status_int, 302)
        self.assertEqual(res.location, url)

    def test_url_2(self):
        request = testing.DummyRequest()
        url = 'https://github.com/b2renger/TheMidst'
        request.body = url

        result = new_url(request)
        key = result['short']
        self.assertEqual(key, 'b2rengerthemidst-github')
