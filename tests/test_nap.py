
from nap.api import Api

from . import HttpServerTestBase


class TestNap(HttpServerTestBase):

    def test_unallowed_method(self):
        """Tries to use non-existent HTTP method"""
        api = Api('http://localhost:8888')
        with self.assertRaises(AttributeError):
            api.resource.nonexisting()
