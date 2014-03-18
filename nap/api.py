"""
Easy HTTP API calling.

Useful information about dynamic attribute creation:
http://docs.python.org/reference/datamodel.html#customizing-attribute-access
"""

import requests


class Api(object):
    """
    This class has special behaviour with its methods - each attribute
    will be dynamically mapped to a Resource instance.
    """

    def __init__(self, api_url, add_trailing_slash=False, **default_kwargs):
        self._api_url = self._ensure_trailing_slash(api_url)
        self._add_trailing_slash = add_trailing_slash
        self._default_kwargs = default_kwargs

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

    def _ensure_trailing_slash(self, text):
        return text if text.endswith('/') else text + '/'

    def _remove_leading_slash(self, text):
        return text[1:] if text.startswith('/') else text

    def _new_resource(self, resource):
        """Create new Resource object with correct url."""
        resource_name = self._remove_leading_slash(resource)
        if self._add_trailing_slash:
            resource_name = self._ensure_trailing_slash(resource_name)

        return Resource(self._api_url + resource_name, self)


class Resource(object):

    # Allowed methods from requests call API
    ALLOWED_METHODS = [
        'HEAD',
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE'
    ]

    def __init__(self, full_url, api):
        self._full_url = full_url
        self._api = api

    def __getattr__(self, method):
        """If class' attribute is accessed and it does not exist, this
        method will be called.
        """
        http_method = method.upper()
        if http_method not in self.ALLOWED_METHODS:
            raise AttributeError('%r object has no attribute %r' %
                                 (self.__class__.__name__, method))

        def wrapper(**kwargs):
            # Add default kwargs with possible custom kwargs returned by
            # before_request
            new_kwargs = self._api.default_kwargs().copy()
            custom_kwargs = self._api.before_request(
                http_method,
                kwargs.copy()
            )
            new_kwargs.update(custom_kwargs)

            response = requests.request(
                http_method,
                self._full_url,
                **new_kwargs
            )

            return self._api.after_request(response)

        return wrapper
