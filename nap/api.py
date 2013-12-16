"""
Easy HTTP API calling.

Useful information about dynamic attribute creation:
http://docs.python.org/reference/datamodel.html#customizing-attribute-access
"""

import requests


class Api(object):

    def __init__(self, api_url, **request_kwargs):
        self._api_url = self._ensure_trailing_slash(api_url)
        self._request_kwargs = request_kwargs

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

    def before_request(self, request_kwargs, method):
        """This method can be used to customize each request.

        request_kwargs must be returned. It is used when calling HTTP method
        for resource.
        """
        return request_kwargs

    def _ensure_trailing_slash(self, text):
        return text if text.endswith('/') else text + '/'

    def _remove_leading_slash(self, text):
        return text[1:] if text.startswith('/') else text

    def _new_resource(self, resource):
        resource_name = self._remove_leading_slash(resource)
        return Resource(
            self._api_url,
            resource_name,
            self._request_kwargs,
            self.before_request)


class Resource(object):

    # Allowed methods from requests call API
    ALLOWED_METHODS = ['head', 'get', 'post', 'put', 'patch', 'delete']

    def __init__(self, api_url, resource, request_kwargs, before_request):
        self._api_url = api_url
        self._resource = resource
        self._request_kwargs = request_kwargs
        self._before_request = before_request

    def __getattr__(self, http_method):
        """If class' attribute is accessed and it does not exist, this
        method will be called.
        """
        if http_method not in self.ALLOWED_METHODS:
            raise AttributeError('%r object has no attribute %r' %
                                 (self.__class__.__http_method__, http_method))

        request_func = getattr(requests, http_method)
        def wrapper(*args, **kwargs):
            full_url = self._api_url + self._resource
            print full_url
            new_kwargs = dict(self._request_kwargs.items() + kwargs.items())
            new_kwargs = self._before_request(new_kwargs, http_method)
            response = request_func(full_url, *args, **new_kwargs)
            return response

        return wrapper
