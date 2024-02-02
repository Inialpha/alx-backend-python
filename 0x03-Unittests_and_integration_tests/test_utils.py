#!/usr/bin/env python3
""" test module for utils.py """
import unittest
from parameterized import parameterized
from typing import (
    Mapping, Sequence, Any, Dict,
    Union,
    Callable,)
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock, DEFAULT


class TestAccessNestedMap(unittest.TestCase):
    """ test suite for access_nested_map function """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,
                               nested_map: Mapping,
                               path: Sequence,
                               expected: Union[Mapping, int]) -> None:
        """ test case for access_nested_map function with correct outputs """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(
            self, nested_map: Mapping, path: Sequence) -> None:
        """ test test case for access_nested_map function with wrong outputs """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ test suit for get_json function """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: Mapping) -> None:
        """ test the get_json function """
        attr = {'json.return_value': test_payload}
        json = Mock(**{'json.return_value': test_payload})
        with patch('requests.get', return_value=json) as mock_get:
            self.assertEqual(get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """ test the memoize function """

    def test_memoize(self):
        """ test the momoize function """

        class TestClass:
            """ test class for momoization """
            def a_method(self):
                """ test method for momoization """

                return 42

            @memoize
            def a_property(self):
                """ test method for momoization """
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=lambda: 42) as a:
            test = TestClass()
            self.assertEqual(test.a_property(), 42)
            self.assertEqual(test.a_property(), 42)
            a.assert_called_once()
