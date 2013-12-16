# *Have some rest, take a Nap*

Nap provides simple and easy way to request REST API resources.

## Usage

`Nap` takes API's base url as its parameter, e.g. `api = Nap('<api-base-url>')`

Returned object will dynamically map called methods to API resources, e.g. `response = api.resource_name.get()`.

`api.resource_name` object dynamically maps its attributes to [*requests* -methods](http://requests.readthedocs.org/en/latest/api/#requests.head)

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
api = Nap('https://api.github.com/users/', auth=('user', 'pass'))

response = api('kimmobrunfeldt').get()
print response.json()

# You can also override the default keyword arguments afterwords
response = api('kimmobrunfeldt').get(auth=('kimmo', 'password1'))
```