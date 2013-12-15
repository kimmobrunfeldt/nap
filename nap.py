"""
Easy REST API calling.

Useful information about dynamic attribute creation:
http://docs.python.org/reference/datamodel.html#customizing-attribute-access
"""

import requests


class Nap(object):

    def __init__(self, api_url):
        self._api_url = self._ensure_trailing_slash(api_url)

    def __call__(self, resource):
        """Makes it possible to call API resources that are illegal method
        names in Python.
        """
        return self._new_resource(resource)

    def __getattr__(self, name):
        """If class' attribute is accessed and it does not exist, this
        method will be called.
        """
        return self._new_resource(name)

    def _ensure_trailing_slash(self, text):
        return text if text.endswith('/') else text + '/'

    def _new_resource(self, resource):
        resource_name = self._ensure_trailing_slash(resource)
        return Resource(self._api_url, resource_name)


class Resource(object):

    # Allowed methods from requests call API
    ALLOWED_METHODS = ['head', 'get', 'post', 'put', 'path', 'delete']

    def __init__(self, api_url, resource):
        self._api_url = api_url
        self._resource = resource

    def __getattr__(self, name):
        """If class' attribute is accessed and it does not exist, this
        method will be called.
        """
        if name not in self.ALLOWED_METHODS:
            raise AttributeError('%r object has no attribute %r' %
                                 (self.__class__.__name__, name))

        request_func = getattr(requests, name)
        def wrapper(*args, **kwargs):
            full_url = self._api_url + self._resource
            response = request_func(full_url, *args, **kwargs)
            return response

        return wrapper
