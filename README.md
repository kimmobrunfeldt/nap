# Nap

*Tests cover pretty much everything, I'd be surprised if Nap didn't work as supposed to.*

[![Build Status](https://travis-ci.org/kimmobrunfeldt/nap.png?branch=master)](https://travis-ci.org/kimmobrunfeldt/nap)
[![Coverage Status](https://coveralls.io/repos/kimmobrunfeldt/nap/badge.png?branch=master)](https://coveralls.io/r/kimmobrunfeldt/nap?branch=master)
[![Badge fury](https://badge.fury.io/py/nap.png)](https://badge.fury.io/py/nap.png)
[![Badge PyPi](https://pypip.in/d/nap/badge.png)](https://pypip.in/d/nap/badge.png)

*Nap* provides convenient way to request HTTP APIs. After coding a few HTTP API wrapper classes, I decided to code *Nap*. It's is just a small(*~150 loc*) wrapper around [requests][]. Requests is a superb HTTP library, which supports everything you'll need to get things done in today's web.

**Example**

```python
from nap.url import Url
api = Url('https://api.github.com/')
# GET https://api.github.com/users
api.get('users')

users = api.join('users')
# GET https://api.github.com/users/kimmobrunfeldt
users.get('kimmobrunfeldt')

# Another way to make the same request as above:
api.get('users/kimmobrunfeldt')
```

**Get started**

* Look through [examples](#examples)
* See [API documentation](docs/nap-api.md)
* [Dive into code](nap/url.py)


## Install

Python versions 2.6, 2.7, 3.2, 3.3 and PyPy are supported and tested against.

Install latest release with *pip*:

    pip install nap

Install latest development version usin *pip*:

    pip install git+git://github.com/kimmobrunfeldt/nap.git

Install latest development version using *setup.py*:

    git clone git@github.com:kimmobrunfeldt/nap.git
    cd nap
    python setup.py install

## Nap API documentation

See [API documentation](docs/nap-api.md)

## Examples

Example with authentication. All authentications supported by *requests* are automatically supported.

```python
from nap.url import Url
users = Url('https://api.github.com/users/')

response = users.get('kimmobrunfeldt', auth=('user', 'pass'))
print(response.json())
```

You can also specify default keyword arguments to be passed on every request in *Url* initialization:

```python
from nap.url import Url
# Keyword arguments given to Url will be given to each request method
# by default for every request.
api = Url('https://api.github.com/', auth=('user', 'pass'))

# Get authenticated user
response = api.get('user')
print(response.json())

# You can also override the default keyword arguments afterwords
response = api.get('users/kimmobrunfeldt', auth=('kimmo', 'password1'))
```

**A bit more complicated example.**
Automatically convert all JSON responses to Python dict objects.
Demonstrate various HTTP methods.
Also raise errors from other than `200 OK` responses.

```python
from nap.url import Url
import requests

class JsonApi(Url):
    def after_request(self, response):
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

# Use https://github.com/kennethreitz/httpbin for testing
api = JsonApi('http://httpbin.org/')

# response is dict object containing parsed JSON
response = api.post('post', data={'test': 'Test POST'})
print(response)

response = api.put('put', data={'test': 'Test PUT'})
print(response)

try:
    # httpbin will response with `Method Not Allowed` if we try to do
    # POST http://httpbin.org/get
    api.post('get')
except requests.exceptions.HTTPError as e:
    print('Response was not OK, it was: %s' % e.response.status_code)
```


## Contributing

[Documentation for Nap developers](docs/)

[requests]: http://docs.python-requests.org/en/latest/     "Requests"
