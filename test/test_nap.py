"""
Tests for nap module.

These tests only focus that requests is called properly.
Everything related to HTTP requests should be tested in requests' own tests.
"""

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
