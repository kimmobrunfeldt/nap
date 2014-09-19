"""
Tests for nap module.

These tests only focus that requests is called properly.
Everything related to HTTP requests should be tested in requests' own tests.
"""

from mock import MagicMock, patch
import unittest
import requests

from nap.url import Url


class NewUrl(Url):

    def before_request(self, method, relative_url, request_kwargs):
        if relative_url.startswith('resource'):
            request_kwargs['relative_url'] = True

        request_kwargs['test'] = 'test'
        return request_kwargs

    def after_request(self, response):
        return None

    def default_kwargs(self):
        # Remove all default kwargs
        return {}


class TestNapExtendBehavior(unittest.TestCase):

    @patch('requests.request')
    def test_before_request_and_after_request(self, r_request):
        """Test overriding before_request() and after_request()"""
        url = NewUrl('http://domain.com')
        r_request = MagicMock(return_value=1)

        # Make sure defaults are passed for each request
        response = url.get('resource')
        requests.request.assert_called_with(
            'GET',
            'http://domain.com/resource',
            test='test',
            relative_url=True
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
        url = NewUrl('http://domain.com', auth=('user', 'pass'))
        r_request = MagicMock(return_value=1)

        # Make sure defaults were removed from kwargs
        url.get('resource')
        requests.request.assert_called_with(
            'GET',
            'http://domain.com/resource',
            # These kwargs will still be set even though default_kwargs
            # is overridden
            test='test',
            relative_url=True
        )
