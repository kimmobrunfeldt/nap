"""
Tests for nap module.

These tests only focus that requests is called properly.
Everything related to HTTP requests should be tested in requests' own tests.
"""

from mock import MagicMock, patch
import unittest
import requests

from nap.api import Api


class TestNap(unittest.TestCase):

    def test_unallowed_method(self):
        """Tries to use non-existent HTTP method"""
        api = Api('')

        # lambda trickery is necessary, because otherwise it would raise
        # AttributeError uncontrolled
        self.assertRaises(AttributeError, lambda: api.resource.nonexisting)

    def test_requests_raises_error(self):
        """Test that requests properly raises its own errors

        >>> requests.get('/kk')
        requests.exceptions.MissingSchema: Invalid URL u'/kk':
        No schema supplied. Perhaps you meant http:///kk?
        """
        api = Api('')
        self.assertRaises(requests.exceptions.MissingSchema, api.resource.get)

    def test_resource_not_callable(self):
        """Make sure resource can't be called directly"""
        api = Api('')
        self.assertRaises(TypeError, api.resource)

    @patch('requests.request')
    def test_default_parameters(self, r_request):
        """Test default parameter behavior"""
        api = Api('', auth=('user', 'password'))
        r_request = MagicMock(return_value=None)

        # Make sure defaults are passed for each request
        api.resource.get()
        requests.request.assert_called_with(
            'GET',
            '/resource',
            auth=('user', 'password')
        )

        # Make sure single calls can override defaults
        api.resource.get(auth=('defaults', 'overriden'))
        requests.request.assert_called_with(
            'GET',
            '/resource',
            auth=('defaults', 'overriden')
        )

    @patch('requests.request')
    def test_trailing_slash(self, r_request):
        """Test that trailing slash will be automatically removed/added"""
        api = Api('')
        r_request = MagicMock(return_value=None)

        # By default slash will not modified anyhow
        api('resource').get()
        requests.request.assert_called_with(
            'GET',
            '/resource'
        )

        api('resource/').get()
        requests.request.assert_called_with(
            'GET',
            '/resource/'
        )

        api_add_slash = Api('', add_trailing_slash=True)
        api_add_slash('resource').get()
        requests.request.assert_called_with(
            'GET',
            '/resource/'
        )
