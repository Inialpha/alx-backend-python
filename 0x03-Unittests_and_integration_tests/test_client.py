#!/usr/bin/env python3
""" test module for client,py """
from client import GithubOrgClient
from typing import Dict
from unittest import TestCase
from unittest.mock import Mock, patch
from parameterized import parameterized


class TestGithubOrgClient(TestCase):
    """ test suite for GithubOrgClient """
    @parameterized.expand([('google',
                          {'client': 'google'}), ('abc', {'client': 'abc'})])
    @patch("client.get_json")
    def test_org(self, org: str, res: Dict, mock: Mock) -> None:
        """ test org method """
        mock.return_value = Mock(return_value=res)
        my_client = GithubOrgClient(org)
        self.assertEqual(my_client.org(), res)
        mock.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org))
