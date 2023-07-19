class GolemioClientError(Exception):
    """
    Base class for exceptions related to GolemioClient.
    """

    def __init__(self, message):
        """
        Initialize a new instance of GolemioClientError.

        Args:
            message (str): The error message.
        """
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(GolemioClientError):
    """
    Exception raised when receiving a 401 - Unauthorized error.
    """

    def __init__(self, message):
        """
        Initialize a new instance of UnauthorizedError.

        Args:
            message (str): The error message.
        """
        super().__init__(message)


class NotFoundError(GolemioClientError):
    """Exception raised when receiving a 404 - Not Found error."""

    def __init__(self, message):
        super().__init__(message)
