#!/usr/bin/env python3
""" test module for client.py """
from client import GithubOrgClient
from typing import Dict
from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock, MagicMock
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

    def test_public_repos_url(self) -> None:
        """ test public_repos_url """

        with patch(
                'client.GithubOrgClient.org',
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': 'google'}
            self.assertEqual(
                GithubOrgClient("wtf")._public_repos_url, 'google')

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """ test cases for public_repos """
        pay_load = [{"repos_url": "https://api.github.com/orgs/google/repos"},
                    [
                    {
                        "id": 7697149,
                        "name": "episodes.dart",
                        "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                        "license": {
                            "key": "bsd-3-clause",
                        }
                    },
                    {
                        "id": 7776515,
                        "name": "cpp-netlib",
                        "full_name": "google/cpp-netlib",
                        "license": {
                            "key": "bsl-1.0"
                        }
                    }
                    ]
                    ]
        mock_get_json.return_value = pay_load[1]
        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = pay_load[0]['repos_url']
            self.assertEqual(
                GithubOrgClient('wtf').public_repos("bsl-1.0"),
                ["cpp-netlib"])
            mock_org.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([(
        {"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)])
    def test_has_license(
            self,
            repo: Dict[str, Dict],
            license_key: str,
            expected: bool) -> None:
        """ test cases for has_license method """
        self.assertEqual(
            GithubOrgClient('tech').has_license(
                repo, license_key), expected)
