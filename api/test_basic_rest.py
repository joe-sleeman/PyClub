"""Tests for basic REST API"""
import json
import unittest
from basic_restful_api import APP


class WebApiTests(unittest.TestCase):
    """Test the two basic REST endpoints - ping/healthcheck"""

    def test_ping(self):
        """Ping"""

        # Get a response from the API
        response = APP.test_client().get("ping")

        # Define our expected & actual
        expected = "200 OK"
        actual = response.status

        # Check
        self.assertEqual(expected, actual)

    def test_healthcheck(self):
        """Healthcheck"""

        # Get a response from the API
        response = APP.test_client().get("healthcheck")

        # Define expected & actual
        expected = "200 OK"
        actual = response.status

        # Check result
        self.assertEqual(expected, actual)

        # Redefine expected & actual
        expected = {'Healthcheck': 'All good!'}
        # Load response data into json as actual
        actual = json.loads(response.data)

        # Check result
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
