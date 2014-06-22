"""
Tests for nap module.

These tests only focus that requests is called properly.
Everything related to HTTP requests should be tested in requests' own tests.
"""

from mock import MagicMock, patch, Mock
import unittest
import requests

from nap.url import Url


class TestNap(unittest.TestCase):

    @patch('requests.session', return_value=Mock(spec_set=requests.Session()))
    def test_join_urls(self, mocked_session):
        """Test creating new sub-Urls"""
        url = Url('http://domain.com')

        new_url = url.join('/path/a/b')
        new_url.get()
        url._session.request.assert_called_with(
            'GET',
            'http://domain.com/path/a/b'
        )

    @patch('requests.session', return_value=Mock(spec_set=requests.Session()))
    def test_joined_urls_option_passing(self, mocked_session):
        """Test that original options are correctly passed to joined urls"""
        url = Url(
            'http://domain.com',
            auth=('user', 'pass')
        )

        new_url = url.join('path')
        new_url.get()
        url._session.request.assert_called_with(
            'GET',
            'http://domain.com/path',
            auth=('user', 'pass')
        )

    @patch('requests.session', return_value=Mock(spec_set=requests.Session()))
    def test_join_url_preserves_original_url(self, mocked_session):
        """Test that original url is not touched when joining urls."""
        url = Url('http://domain.com/')

        new_url = url.join('/path')
        new_url.get()
        url._session.request.assert_called_with(
            'GET',
            'http://domain.com/path'
        )

        new_url = url.join('/path/')
        new_url.get()
        url._session.request.assert_called_with(
            'GET',
            'http://domain.com/path/'
        )

    def test_requests_raises_error(self):
        """Test that requests properly raises its own errors

        >>> requests.get('/kk')
        requests.exceptions.MissingSchema: Invalid URL u'/kk':
        No schema supplied. Perhaps you meant http:///kk?
        """
        url = Url('')
        self.assertRaises(requests.exceptions.MissingSchema, url.get)

    @patch('requests.session', return_value=Mock(spec_set=requests.Session()))
    def test_default_parameters(self, mocked_session):
        """Test default parameter behavior"""
        url = Url('http://domain.com', auth=('user', 'password'))

        # Make sure defaults are passed for each request
        url.get('resource')
        url._session.request.assert_called_with(
            'GET',
            'http://domain.com/resource',
            auth=('user', 'password')
        )

        # Make sure single calls can override defaults
        url.get('resource', auth=('defaults', 'overriden'))
        url._session.request.assert_called_with(
            'GET',
            'http://domain.com/resource',
            auth=('defaults', 'overriden')
        )

    def test_url_getter_setter(self):
        """Test url attribute"""
        base_url = 'http://domain.com'
        url = Url(base_url)

        self.assertEqual(url.url, base_url)

        # Inline function definition instead of using with keyword to support
        # python 2.6 unittest module
        def test_set(url):
            url.url = 'http://newdomain.com'

        # url attribute should be read-only
        self.assertRaises(AttributeError, test_set, url)

    @patch('requests.session', return_value=Mock(spec_set=requests.Session()))
    def test_all_methods(self, mocked_session):
        """Test all HTTP methods"""
        url = Url('http://domain.com')
        self._test_all_methods(url, 'http://domain.com')

        new_url = url.join('path/a/b')
        self._test_all_methods(new_url, 'http://domain.com/path/a/b')

    def _test_all_methods(self, url_obj, expected_url):
        """Test all methods for given url object"""
        methods = ['delete', 'get', 'head', 'patch', 'post', 'put']

        for method in methods:
            getattr(url_obj, method.lower())()

            url_obj._session.request.assert_called_with(
                method.upper(),
                expected_url
            )

    def test_all_methods_with_custom_session(self):
        """Test all HTTP methods"""
        session = Mock(spec_set=requests.Session())
        url = Url('http://domain.com', session=session)
        self._test_all_methods_with_custom_session(url, 'http://domain.com', session)

        new_url = url.join('path/a/b')
        self._test_all_methods_with_custom_session(new_url, 'http://domain.com/path/a/b', session)

    def _test_all_methods_with_custom_session(self, url_obj, expected_url, session):
        """Test all methods for given url object"""

        methods = ['delete', 'get', 'head', 'patch', 'post', 'put']

        for method in methods:
            getattr(url_obj, method.lower())()

            url_obj._session.request.assert_called_with(
                method.upper(),
                expected_url
            )