# Nap

[![Build Status](https://travis-ci.org/kimmobrunfeldt/nap.png?branch=master)](https://travis-ci.org/kimmobrunfeldt/nap)
[![Coverage Status](https://coveralls.io/repos/kimmobrunfeldt/nap/badge.png?branch=master)](https://coveralls.io/r/kimmobrunfeldt/nap?branch=master)
[![Badge fury](https://badge.fury.io/py/nap.png)](https://badge.fury.io/py/nap.png)
[![Badge PyPi](https://pypip.in/d/nap/badge.png)](https://pypip.in/d/nap/badge.png)

*Nap* provides simple and easy way to request HTTP API resources. After coding a few HTTP API wrapper classes, I decided to code *Nap*. It's is just a small(*~100 loc*) wrapper around [requests][].

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

**Get started**

* Look through [examples](#examples)
* See [API documentation](docs/nap-api.md)
* [Dive into code](nap/api.py)


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

## Contributing

[Documentation for Nap developers](docs/)

[requests]: http://docs.python-requests.org/en/latest/     "Requests"
