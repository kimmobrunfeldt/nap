"""
Easy HTTP API calling.
"""

import sys

_PY3 = sys.version_info >= (3, 0)

# For Python 3 compatibility
if _PY3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

import requests


class Url(object):
    """Wrapper class for requests library."""

    def __init__(self, url, **default_kwargs):
        """
        `url`
            API's base url. Trailing slash is optional.
            For example `'https://api.github.com'`

        `**default_kwargs`
            Keyword arguments that will be passed to
            `requests.request` on each request
        """
        self._url = url
        self._default_kwargs = default_kwargs

    def before_request(self, method, request_kwargs):
        """This method can be overridden to customize each request.
        Note: request_kwargs contains ONLY the kwargs that were straightly
        given in the call. Example: `api.resource.get(kwarg1=1)` the dict
        would be: `{'kwarg1': 1}`

        request_kwargs must be returned. It is used when calling HTTP method
        for resource. These returned kwargs will be added on top of
        self._default_kwargs.
        """
        return request_kwargs

    def after_request(self, response):
        """This method can be overridden to add default behavior when response
        is returned. For example if you're working with a JSON API, you can
        return deserialized JSON from this method instead of `Response` object.
        The returned value will be returned to HTTP method caller.
        """
        return response

    def default_kwargs(self):
        """Returns kwargs which are default for each request. This can
        be overridden to modify default kwargs.
        """
        return self._default_kwargs

    def join(self, relative_url):
        """Join initial url with a new relative url and return new Url object
        from the combined url.
        """
        return self._new_url(relative_url)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def head(self, *args, **kwargs):
        return self.request('HEAD', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def request(self, http_method, relative_url='', **kwargs):
        """Does actual HTTP request using requests library."""
        # It could be possible to call api.resource.get('/index')
        # but it would be non-intuitive that the path would resolve
        # to root of domain
        relative_url = self._remove_leading_slash(relative_url)

        # Add default kwargs with possible custom kwargs returned by
        # before_request
        new_kwargs = self.default_kwargs().copy()
        custom_kwargs = self.before_request(
            http_method,
            kwargs.copy()
        )
        new_kwargs.update(custom_kwargs)

        response = requests.request(
            http_method,
            self._join_url(relative_url),
            **new_kwargs
        )

        return self.after_request(response)

    def _join_url(self, relative_url):
        """Joins relative url with base url. Adds trailing slash if needed."""
        joined_url = urljoin(self._url, relative_url)
        return joined_url

    def _remove_leading_slash(self, text):
        return text[1:] if text.startswith('/') else text

    def _new_url(self, relative_url):
        """Create new Url which points to new url."""

        return Url(
            urljoin(self._url, relative_url),
            **self._default_kwargs
        )
