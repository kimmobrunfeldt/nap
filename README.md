# Nap

*Tests cover pretty much everything, I'd be surprised if it didn't work as supposed to.*

[![Build Status](https://travis-ci.org/kimmobrunfeldt/nap.png?branch=master)](https://travis-ci.org/kimmobrunfeldt/nap)
[![Coverage Status](https://coveralls.io/repos/kimmobrunfeldt/nap/badge.png?branch=master)](https://coveralls.io/r/kimmobrunfeldt/nap?branch=master)
[![Badge fury](https://badge.fury.io/py/nap.png)](https://badge.fury.io/py/nap.png)
[![Badge PyPi](https://pypip.in/d/nap/badge.png)](https://pypip.in/d/nap/badge.png)

*Nap* provides convenient way request HTTP APIs. After coding a few HTTP API wrapper classes, I decided to code *Nap*. It's is just a small(*~150 loc*) wrapper around [requests][].

**Example**

```python
from nap.url import Url
api = Url('https://api.github.com/')
# GET https://api.github.com/users
api.get('users')

users = api.join('users')
# GET https://api.github.com/users/kimmobrunfeldt
users.get('kimmobrunfeldt')

# Or you could just call
api.get('users/kimmobrunfeldt')
```

**Get started**

* Look through [examples](#examples)
* See [API documentation](docs/nap-api.md)
* [Dive into code](nap/url.py)


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

Automatically convert all JSON responses to Python dict objects

```python
from nap.url import Url

class JsonApi(Url):
    def after_request(self, response):
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

api = JsonApi('https://api.github.com/')

# Get authenticated user
user = api.get('users')  # user is dict object containing parsed JSON
print(user)
```


## Contributing

[Documentation for Nap developers](docs/)

[requests]: http://docs.python-requests.org/en/latest/     "Requests"
