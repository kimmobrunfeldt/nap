## Nap API documentation

Reference documentation

### [nap.api.Api(api_url, trailing_slash=False, \*\*request_kwargs)](/nap/api.py)

* `api_url` API's base url. Trailing slash is optional. For example `'https://api.github.com'`
* `trailing_slash` If *True*, every request will contain trailing slash in the final requested url.
    Trailing slash `https://api.github.com/users/`. No trailing slash `https://api.github.com/users`.
* `**request_kwargs` Keyword arguments that will be passed to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.head) on each request

This class has special behaviour with its methods - each method will be dynamically mapped to a [Resource](#napapiresourceapi_url-resource-request_kwargs-before_request-after_request) instance.

You can reference to resource in two ways
```python
api.resource.get()
api('resource').get()
# The second way makes it possible to request url paths like:
# api('resource/path').get()
```

#### Api.before_request(request_kwargs, method)

* `request_kwargs` Keyword arguments that were passed to the request method. This does not contain the default keyword arguments given when initializing Api class. For example in `api.resource.get(verify=False)`, the value would be `{'verify': False}`.
* `method` The HTTP method of request in lower case. For example `'get'`.

This method should return keyword arguments. These returned kwargs will be added on top of default request_kwargs given to class. The sum of both keyword arguments will be passed to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.head).

#### Api.after_request(response)

* `response` [Response](http://docs.python-requests.org/en/latest/api/#requests.Response) object returned by request

This method can be used to add default behavior for response modification. For example if you're working with a JSON API, you can return deserialized JSON from this method instead of `Response` object.

The returned value will be returned to the API method caller: `api.users.get()`.

### [nap.api.Resource(api_url, resource, request_kwargs, before_request, after_request)](/nap/api.py#L69)

* `api_url` Base url of the API
* `resource` Resource path. Examples: `'users'`, `'users/list'`.
* `request_kwargs` Default kwargs to be given to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.head) on each request.
* `before_request` See [before_request()](#apibefore_requestrequest_kwargs-method)
* `after_request` See [after_request()](#apiafter_requestresponse)

The only difference to [requests' methods](http://docs.python-requests.org/en/latest/api/#requests.head) is that the first *url* parameter is passed automatically. You only need to pass the keyword arguments.

#### Resource.head(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.head

#### Resource.get(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.get

#### Resource.post(data=None, **kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.post

#### Resource.put(data=None, **kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.put

#### Resource.patch(data=None, **kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.patch

#### Resource.delete(**kwargs)

http://docs.python-requests.org/en/latest/api/#requests.delete
