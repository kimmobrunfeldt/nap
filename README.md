# Nap

[![Build Status](https://travis-ci.org/kimmobrunfeldt/nap.png?branch=master)](https://travis-ci.org/kimmobrunfeldt/nap)
[![Coverage Status](https://coveralls.io/repos/kimmobrunfeldt/nap/badge.png?branch=master)](https://coveralls.io/r/kimmobrunfeldt/nap?branch=master)
[![Badge fury](https://badge.fury.io/py/nap.png)](https://badge.fury.io/py/nap.png)
[![Badge PyPi](https://pypip.in/d/nap/badge.png)](https://pypip.in/d/nap/badge.png)

*Nap* provides simple and easy way to request HTTP API resources. After coding a few HTTP API wrapper classes, I decided to code *Nap*. It's is just a small(*~100 loc*) wrapper around [requests](http://requests.readthedocs.org).

With *Nap*, you don't need to create methods for every single resource in the API. See the [example case](#example-case) for more. Shortly the reasoning is:

**Bad**

```python
class Api(object):
    api_url = 'https://www.bitstamp.net/api/'

    def ticker(self):
        return self._get('ticker')

    def conversion_rate_usd_eur(self):
        return self._get('eur_usd')

    # ... methods for all API resources ...
```

**Better**

```python
from nap.api import Api
api = Api('https://www.bitstamp.net/api/')

# That's it! Now you can call methods on API resources
api.ticker.get()
api.eur_usd.get()
```

#### *Stop coding needless code - have a Nap.*

## Install

Python versions 2.6 - 3.3 are supported and tested against.

Install latest release with *pip*:

    pip install nap

Install latest development version usin *pip*:

    pip install git+git://github.com/kimmobrunfeldt/nap.git

Install latest development version using *setup.py*:

    git clone git@github.com:kimmobrunfeldt/nap.git
    cd nap
    python setup.py install

## Nap reference

API reference

### [nap.api.Api(*api_url, trailing_slash=False, \*\*request_kwargs*)](nap/api.py)

* *api_url* - API's base url. Trailing slash is optional. For example *https://api.github.com*
* *trailing_slash* - If True, every request will contain trailing slash in the final requested url.
    Trailing slash *https://api.github.com/users/*. No trailing slash *https://api.github.com/users*.
* *\*\*request_kwargs* - Keyword arguments that will be passed to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.head) on each request

For example
```python
api = Api('https://api.github.com')
```

This class has special behaviour with its methods - each method will be dynamically mapped to a [Resource]() instance. For example
```python
users = api.users
```

Now users variable is instance of [Resource]() and all HTTP methods can be called for the instance, like this
```python
users.get()
```
#### .before_request(*request_kwargs, method*)

* *request_kwargs* - Keyword arguments that were passed to the request method. This does not contain the default keyword arguments given when initializing Api class. For example in `api.resource.get(verify=False)`, the value would be `{'verify': False}`.
* *method* - The HTTP method of request in lower case. For example `get`.

This method should return keyword arguments. These returned kwargs will be added on top of default request_kwargs given to class. The sum of both keyword arguments will be passed to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.head).

#### .after_request(*response*)

* *response* - [Response](http://docs.python-requests.org/en/latest/api/#requests.Response) object returned by request

This method can be used to add default behavior for response modification. For example if you're working with a JSON API, you can return deserialized JSON from this method instead of `Response` object.

The returned value will be returned to the API method caller: `api.users.get()`.

### [nap.api.Resource(*api_url, resource, request_kwargs, before_request, after_request*)](nap/api.py#L69)

* *api_url* - Base url of the API
* *resource* - Resource path. Examples: `users`, `users/list`.
* *request_kwargs* - Default kwargs to be given to [requests' method](http://docs.python-requests.org/en/latest/api/#requests.head) on each request.
* *before_request* - See [before_request()]
* *after_request* - See [after_request()]

The only difference to [requests' methods](http://docs.python-requests.org/en/latest/api/#requests.head) is that the first *url* parameter is passed automatically. You only need to pass the keyword arguments.

#### .head(*\*\*kwargs*)

See http://docs.python-requests.org/en/latest/api/#requests.head

#### .get(*\*\*kwargs*)

See http://docs.python-requests.org/en/latest/api/#requests.get

#### .post(*data=None, \*\*kwargs*)

See http://docs.python-requests.org/en/latest/api/#requests.post

#### .put(*data=None, \*\*kwargs*)

See http://docs.python-requests.org/en/latest/api/#requests.put

#### .patch(*data=None, \*\*kwargs*)

See http://docs.python-requests.org/en/latest/api/#requests.patch

#### .delete(\*\*kwargs*)

http://docs.python-requests.org/en/latest/api/#requests.delete

## Examples

Get EUR to USD conversion rates from [Bitstamp API](https://www.bitstamp.net/api/).

```python
from nap.api import Api
api = Api('https://www.bitstamp.net/api/')

response = api.eur_usd.get()
print(response.json())
```

Example with authentication. All authentications supported by *requests* are automatically supported.

```python
from nap.api import Api
api = Api('https://api.github.com/users/')

response = api('kimmobrunfeldt').get(auth=('user', 'pass'))
print(response.json())
```

You can also specify default keyword arguments to be passed on every request in Api initialization:

```python
from nap.api import Api
# Keyword arguments given to Api will be given to each request method
# by default for every request.
api = Api('https://api.github.com/', auth=('user', 'pass'))

response = api('user').get()
print(response.json())

# You can also override the default keyword arguments afterwords
response = api('users/kimmobrunfeldt').get(auth=('kimmo', 'password1'))
```

## Example case

Let's take [bitstamp-python-client](https://github.com/kmadac/bitstamp-python-client/) for an example. It contains client code for [Bitstamp's public API](https://www.bitstamp.net/api/).

The whole [public -class](https://github.com/kmadac/bitstamp-python-client/blob/4cefe8ffb29cac385f018bc836376d21147b1562/bitstamp/client.py#L9) can be squeezed to quite minimal code with *Nap*:

```python
from nap.api import Api

# Let's use incorrect naming(PEP8) to mimic the code in *bitstamp-python-client*
class public(Api):

    # This will take all keyword arguments given to `nap.api.Api.resource.get()`
    # and assume they are parameters for the HTTP request, not parameters
    # to be passed to `requests` module.
    def before_request(self, kwargs, method):
        return {'params': kwargs}

    def after_request(self, response):
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

```

Now it is possible to call all Bitstamp public API resources. The only major difference is that you have to use same parameter names as Bitstamp's API.

```python
proxydict = None
api = public('https://www.bitstamp.net/api/', proxies=proxydict)

# Returns JSON dictionary with "bids" and "asks".
# group - group orders with the same price (0 - false; 1 - true). Default: 1.
api.order_book.get(group=0)

api.transactions.get(time="minute")

```

## Makefile

All `make` tasks:

    clean - execute all clean tasks
    clean-build - remove build artifacts
    clean-pyc - remove Python file artifacts
    clean-coverage - remove coverage artifacts
    lint - check style with flake8
    test - run tests quickly with the default Python
    test-all - run tests on every Python version with tox
    coverage - check code coverage quickly with the default Python
    release - package and upload a release
    dist - package

## Contributing

[Docs for developers](docs/)

## License(MIT)

    Copyright (C) 2013 Kimmo Brunfeldt

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


    [requests]: http://docs.python-requests.org/en/latest/     "Requests"
