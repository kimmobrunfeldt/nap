# Nap API documentation

Reference documentation

## nap.url

### [class Url(base_url, \*\*default_kwargs)](/nap/url.py#L20)

* `base_url`
    Base url. Trailing slash is optional.
    For example `'https://api.github.com'`

* `**default_kwargs`
    Keyword arguments that will be passed to
    [requests.request][] on each request

**Example**
```python
from nap.url import Url
api = Url('https://api.github.com/', auth=('kimmo', 'pass'))
```

#### .url

This attribute can be used to read base url. Read-only.

#### .join(relative_url='')

Joins base url with `relative_url` and returns new [Url](#class-urlurl-default_kwargs) instance
initialized with the combined url.

All `default_kwargs` given in first initialization are passed to new *Url* instance.

```python
api = Url('https://api.github.com/', auth=('kimmo', 'pass'))
users = api.join('users')
```

#### .head(relative_url='', **kwargs)

Uses [requests.request][] to send `HEAD` request.

* `relative_url`
    Relative url to base url which should be requested.

* `**kwargs`
    Keyword arguments are passed to *requests.request* function.
    Check [requests.request][] documentation.

```python
api.head('path')  # HEAD https://api.github.com/path
```

#### .get(relative_url='', **kwargs)

Uses [requests.request][] to send `GET` request.

* `relative_url`
    Relative url to base url which should be requested.

* `**kwargs`
    Keyword arguments are passed to *requests.request* function.
    Check [requests.request][] documentation.

```python
api.get('path')  # GET https://api.github.com/path
```

#### .post(relative_url='', **kwargs)

Uses [requests.request][] to send `POST` request.

* `relative_url`
    Relative url to base url which should be requested.

* `**kwargs`
    Keyword arguments are passed to *requests.request* function.
    Check [requests.request][] documentation.

```python
api.post('path')  # POST https://api.github.com/path
```

#### .put(relative_url='', **kwargs)

Uses [requests.request][] to send `PUT` request.

* `relative_url`
    Relative url to base url which should be requested.

* `**kwargs`
    Keyword arguments are passed to *requests.request* function.
    Check [requests.request][] documentation. that `url` and `method` parameters are passed automatically.

```python
api.put('path')  # PUT https://api.github.com/path
```

#### .patch(relative_url='', **kwargs)

Uses [requests.request][] to send `PATCH` request.

* `relative_url`
    Relative url to base url which should be requested.

* `**kwargs`
    Keyword arguments are passed to *requests.request* function.
    Check [requests.request][] documentation.

```python
api.patch('path')  # PATCH https://api.github.com/path
```

#### .delete(relative_url='', **kwargs)

Uses [requests.request][] to send `DELETE` request.

* `relative_url`
    Relative url to base url which should be requested.

* `**kwargs`
    Keyword arguments are passed to *requests.request* function.
    Check [requests.request][] documentation.

```python
api.delete('path')  # DELETE https://api.github.com/path
```

#### .before_request(method, relative_url, request_kwargs)

This method can be overridden to customize each request.

* `method`
    The HTTP method of request in upper case. For example `'GET'`.

* `relative_url`
    The relative URL passed to the HTTP method, without leading slash.

* `request_kwargs`
    Keyword arguments that were passed to the request method.
    This does not contain the default keyword arguments given when
    initializing Api class. For example in `url.get(verify=False)`,
    the value would be `{'verify': False}`.

This method should return keyword arguments. These returned kwargs will be
added on top of default request_kwargs given to class. The sum of both keyword
arguments will be passed to [requests.request][].

#### .after_request(response)

This method can be overridden to add default behavior when response
is returned. For example if you're working with a JSON API, you can
return deserialized JSON from this method instead of `Response` object.

* `response`
    [Response](http://docs.python-requests.org/en/latest/api/#requests.Response)
    object returned by *request* function

The returned value will be returned to the API method caller:
`response = api.get('users')`.

#### .default_kwargs()

This method can be overridden to modify `default_kwargs` given in class initialization.

Returns new default kwargs.


[requests.request]: http://docs.python-requests.org/en/latest/api/#requests.request     "requests.request"
