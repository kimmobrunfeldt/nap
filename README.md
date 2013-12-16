# Nap

*Nap* provides simple and easy way to request HTTP API resources.

After coding a few HTTP API wrapper classes, I decided to code *Nap*. With *Nap*, you don't need to create methods for every single resource in the API.

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

Python versions 2.6 - 3.3 are supported.

Install with *pip*:

    pip install nap

Using *setup.py*:

    git clone git@github.com:kimmobrunfeldt/nap.git
    cd nap
    python setup.py install

## Usage

`nap.api.Api` takes API's base url as its parameter, e.g. `api = Api('<api-base-url>')`. If your API's resources have trailing slash in their url, it can be enforced with `Api('<api-base-url>', trailing_slash=True)`.

Returned object will dynamically map called methods to API resources, e.g. `resource = api.resource_name`.

`resource` has all HTTP methods which can be called naturally: `resource.get()`. The methods are dynamically mapped to [*requests* -methods](http://requests.readthedocs.org/en/latest/api/#requests.head). You just don't need to specify the *url* parameter.

HTTP method call will return requests' [Response object](http://requests.readthedocs.org/en/latest/api/#requests.Response): `response = resource.get()`.

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

The whole [public -class](https://github.com/kmadac/bitstamp-python-client/blob/master/bitstamp/client.py#L9) can be squeezed to quite minimal code with *Nap*:

```python
# Let's use incorrect naming(PEP8) to mimic the code in *bitstamp-python-client*
class public(Api):

    # This will take all keyword arguments given to `nap.api.Api.resource.get()`
    # and assume they are parameters for the HTTP request, not parameter
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

## License(MIT)

    Copyright (C) 2013 Kimmo Brunfeldt

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.