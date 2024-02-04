#!/usr/bin/env python3
""" test module for client.py """
from client import GithubOrgClient
from typing import Dict
from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class

from fixtures import TEST_PAYLOAD

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
                GithubOrgClient('wtf').public_repos(),
                ["episodes.dart", "cpp-netlib"])
            mock_org.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([(
        {"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),])
    
    def test_has_license(
            self,
            repo: Dict[str, Dict],
            license_key: str,
            expected: bool) -> None:
        """ test cases for has_license method """
        instance = GithubOrgClient("tech")
        output = instance.has_license(repo, license_key)
        self.assertEqual(output, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(TestCase):
    """ TestIntegrationGithubOrgClient class """

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()
