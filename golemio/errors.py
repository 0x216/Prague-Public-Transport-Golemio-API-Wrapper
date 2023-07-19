class GolemioClientError(Exception):
    """Базовый класс для исключений, связанных с GolemioClient."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(GolemioClientError):
    """Исключение, возникающее при получении ошибки 401 - Unauthorized."""

    def __init__(self, message):
        super().__init__(message)


class NotFoundError(GolemioClientError):
    """Исключение, возникающее при получении ошибки 404 - Not Found."""

    def __init__(self, message):
        super().__init__(message)