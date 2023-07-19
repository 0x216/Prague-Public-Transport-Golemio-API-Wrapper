import unittest
from golemio.client import GolemioClient
from golemio.errors import GolemioClientError, NotFoundError, UnauthorizedError


class GolemioClientTests(unittest.TestCase):
    def setUp(self):
        # In debug mode we don't need to use api key
        self.client = GolemioClient('', debug=True)

    def test_getRoutes(self):
        routes = self.client.getRoutes()
        self.assertIsInstance(routes, list)

    def test_getRoutes_unauthorized(self):
        # Создаем клиента без API ключа, чтобы вызвать ошибку UnauthorizedError
        client = GolemioClient(api_key=None, debug=False)
        with self.assertRaises(UnauthorizedError):
            client.getRoutes()

    def test_getRoute_not_found(self):
        # Задаем несуществующий route_id, чтобы вызвать ошибку NotFoundError
        route_id = 'non_existent_route'
        with self.assertRaises(NotFoundError):
            self.client.getRoute(route_id)
