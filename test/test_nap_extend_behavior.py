"""
Tests for nap module.

These tests only focus that requests is called properly.
Everything related to HTTP requests should be tested in requests' own tests.
"""

from mock import MagicMock, patch
import unittest
import requests

from nap.api import Api


class NewApi(Api):

    def before_request(self, method, request_kwargs):
        request_kwargs['test'] = 'test'
        return request_kwargs

    def after_request(self, response):
        return None

    def default_kwargs(self):
        # Remove all default kwargs
        return {}


class TestNapInherit(unittest.TestCase):

    @patch('requests.request')
    def test_before_request_and_after_request(self, r_request):
        """Test overriding before_request() and after_request()"""
        api = NewApi('')
        r_request = MagicMock(return_value=1)

        # Make sure defaults are passed for each request
        response = api.resource.get()
        requests.request.assert_called_with(
            'GET',
            '/resource',
            test='test'
        )

        # Mocker will return 1 to after_request and we have modified it
        # to return just None
        self.assertEquals(
            response,
            None,
            'after_request overriding not working'
        )

    @patch('requests.request')
    def test_default_kwargs(self, r_request):
        """Test overriding default_kwargs()"""
        # We give default arguments, but the overriding implementation
        # of default_kwargs() method should throw them away
        api = NewApi('', auth=('user', 'pass'))
        r_request = MagicMock(return_value=1)

        # Make sure defaults were removed from kwargs
        api.resource.get()
        requests.request.assert_called_with(
            'GET',
            '/resource',
            # This will still be in kwargs because manipulation
            # of default_kwargs and request_kwargs are separated
            test='test'
        )

