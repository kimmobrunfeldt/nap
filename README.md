# Nap

Nap provides simple and easy way to request REST API resources.

After coding a few HTTP API wrapper classes, I decided to code Nap. With Nap, you don't need to create methods for every single resource in the API.

**Bad**

    class Api(object):
        api_url = 'https://www.bitstamp.net/api/'

        def ticker(self):
            return self._get('ticker')

        def conversion_rate_usd_eur(self):
            return self._get('eur_usd')

        # ... methods for all API resources ...

**Better***

    from nap import Nap
    api = Nap('https://www.bitstamp.net/api/')

    # That's it! Now you can call methods on API resources
    api.ticker.get()
    api.eur_usd.get()


## Usage

`Nap` takes API's base url as its parameter, e.g. `api = Nap('<api-base-url>')`

Returned object will dynamically map called methods to API resources, e.g. `resource = api.resource_name`.

`resource` has all HTTP methods which can be called naturally: `resource.get()`. The methods are dynamically mapped to [*requests* -methods](http://requests.readthedocs.org/en/latest/api/#requests.head).

## Examples

Get EUR to USD conversion rates from [Bitstamp API](https://www.bitstamp.net/api/).

```python
from nap import Nap
api = Nap('https://www.bitstamp.net/api/')

response = api.eur_usd.get()
print response.json()
```

Example with authentication. All authentications supported by *requests* are automatically supported.

```python
from nap import Nap
api = Nap('https://api.github.com/users/')

response = api('kimmobrunfeldt').get(auth=('user', 'pass'))
print response.json()
```

You can also pass default keyword arguments to be passed on every request in Nap initialization:

```python
from nap import Nap
# Keyword arguments given to Nap will be given to each request method
# by default for every request.
api = Nap('https://api.github.com/', auth=('user', 'pass'))

response = api('user').get()
print response.json()

# You can also override the default keyword arguments afterwords
response = api('users/kimmobrunfeldt').get(auth=('kimmo', 'password1'))
```