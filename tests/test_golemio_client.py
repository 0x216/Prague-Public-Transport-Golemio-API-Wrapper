import unittest
from golemio.client import GolemioClient
from golemio.errors import GolemioClientError, NotFoundError, UnauthorizedError


class GolemioClientTests(unittest.TestCase):
    """
    Unit tests for the GolemioClient class.
    """

    def setUp(self):
        """
        Set up the test case by creating an instance of GolemioClient.
        """
        # In debug mode we don't need to use an API key
        self.client = GolemioClient('', debug=True)

    def test_getRoutes(self):
        """
        Test the getRoutes method of GolemioClient.
        """
        routes = self.client.getRoutes()
        self.assertIsInstance(routes, list)

    def test_getRoutes_unauthorized(self):
        """
        Test the behavior of getRoutes method when called without an API key.
        It should raise an UnauthorizedError.
        """
        client = GolemioClient(api_key=None, debug=False)
        with self.assertRaises(UnauthorizedError):
            client.getRoutes()

    def test_getRoute_not_found(self):
        """
        Test the behavior of getRoute method when called with a non-existent route_id.
        It should raise a NotFoundError.
        """
        route_id = 'non_existent_route'
        with self.assertRaises(NotFoundError):
            self.client.getRoute(route_id)
