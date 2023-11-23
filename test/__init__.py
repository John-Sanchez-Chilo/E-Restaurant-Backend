import unittest
from .main import RestaurantTestCase

def suite():
    suite = unittest.TestSuite()
    suite.addTest(RestaurantTestCase('test_percentage'))
    return suite