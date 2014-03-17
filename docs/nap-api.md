## Nap API documentation

Reference documentation

### [nap.api.Api(api_url, add_trailing_slash=False, \*\*default_kwargs)](/nap/api.py)

* `api_url` API's base url. Trailing slash is optional. For example `'https://api.github.com'`
* `add_trailing_slash` If *True*, every request will be forced to use trailing slash in the final requested url. By default, trailing slash is not modified at all. You can pass either with or without it.
    Trailing slash `https://api.github.com/users/`. No trailing slash `https://api.github.com/users`. This is useful in cases where you want to call with this style `api.resource.get`, but your API wants trailing slash in request urls.
* `**default_kwargs` Keyword arguments that will be passed to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.request) on each request

This class has special behaviour with its methods - each method will be dynamically mapped to a [Resource](#napapiresourcefull_url-api) instance.

You can reference to resource in two ways
```python
api = Api('http://example.com/api')
api.resource.get()
api('resource').get()
# The second way makes it possible to request url paths like:
# api('resource/path').get()
```

#### Api.before_request(method, request_kwargs)

* `method` The HTTP method of request in upper case. For example `'GET'`.
* `request_kwargs` Keyword arguments that were passed to the request method. This does not contain the default keyword arguments given when initializing Api class. For example in `api.resource.get(verify=False)`, the value would be `{'verify': False}`.

This method should return keyword arguments. These returned kwargs will be added on top of default request_kwargs given to class. The sum of both keyword arguments will be passed to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.request).

#### Api.after_request(response)

* `response` [Response](http://docs.python-requests.org/en/latest/api/#requests.Response) object returned by request

This method can be used to add default behavior for response modification. For example if you're working with a JSON API, you can return deserialized JSON from this method instead of `Response` object.

The returned value will be returned to the API method caller: `api.users.get()`.

#### Api.default_kwargs()

This method can be overridden to modify `default_kwargs` given in class initialization. modification.

Returns new default kwargs.

### [nap.api.Resource(full_url, api)](/nap/api.py#L75)

* `full_url` Full url of the API resource. For example `http://example.com/api/resource`
* `api` Instance of `Api` which implements `before_request()`, `default_kwargs()` and `after_request()`

The only difference to [requests' methods](http://docs.python-requests.org/en/latest/api/#requests.request) is that `url` and `method` parameters are passed automatically. You only need to pass the keyword arguments.

You can also call methods in uppercase, for example `Resource.GET()`.

#### Resource.head(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.request

Only difference is that `url` and `method` parameters are passed automatically.

#### Resource.get(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.request

Only difference is that `url` and `method` parameters are passed automatically.

#### Resource.post(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.request

Only difference is that `url` and `method` parameters are passed automatically.

#### Resource.put(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.request

Only difference is that `url` and `method` parameters are passed automatically.

#### Resource.patch(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.request

Only difference is that `url` and `method` parameters are passed automatically.

#### Resource.delete(**kwargs)

See http://docs.python-requests.org/en/latest/api/#requests.request

Only difference is that `url` and `method` parameters are passed automatically.
