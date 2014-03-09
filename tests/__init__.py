import unittest


class HttpServerTestBase(unittest.TestCase):
    """
    Baseclass which setups a HTTP server for tests to use.
    """

    @classmethod
    def setUpClass(cls):
        print 'Setup server'
        pass

    @classmethod
    def tearDownClass(cls):
        print 'Teardown server'
        pass
