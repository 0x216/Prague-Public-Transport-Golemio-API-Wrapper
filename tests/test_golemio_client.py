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

    def test_getServices(self):
        """
        Test the getServices method of GolemioClient.
        """
        services = self.client.getGTFSServices()
        self.assertIsInstance(services, list)

    def test_getGTFSRoutes(self):
        """
        Test the getGTFSRoutes method of GolemioClient.
        """
        routes = self.client.getGTFSRoutes()
        self.assertIsInstance(routes, list)

    def test_getGTFSRoute(self):
        """
        Test the getGTFSRoute method of GolemioClient.
        """
        routes = self.client.getGTFSRoutes()
        route_id = routes[0]['route_id']
        route = self.client.getGTFSRoute(route_id)
        self.assertIsInstance(route, dict)

    def test_getGTFSTrips(self):
        """
        Test the getGTFSTrips method of GolemioClient.
        """
        trips = self.client.getGTFSTrips()
        self.assertIsInstance(trips, list)

    def test_getGTFSShape(self):
        """
        Test the getGTFSShape method of GolemioClient.
        """
        shape = self.client.getGTFSShape('L991V2')
        self.assertIsInstance(shape, dict)

    def test_getGTFSAllStops(self):
        """
        Test the getGTFSAllStops method of GolemioClient.
        """
        stops = self.client.getGTFSAllStops()
        self.assertIsInstance(stops, dict)

    def test_getRoutes_unauthorized(self):
        """
        Test the behavior of getGTFSRoutes method when called without an API key.
        It should raise an UnauthorizedError.
        """
        client = GolemioClient(api_key=None, debug=False)
        with self.assertRaises(UnauthorizedError):
            client.getGTFSRoutes()

    def test_getGTFSRoute_not_found(self):
        """
        Test the behavior of getGTFSRoute method when called with a non-existent route_id.
        It should raise a NotFoundError.
        """
        route_id = 'non_existent_route'
        with self.assertRaises(NotFoundError):
            self.client.getGTFSRoute(route_id)
