import requests
import urllib.parse
from .errors import *


class GolemioClient(object):
    """
    Python wrapper for the Golemio API.
    """

    def __init__(self, api_key='', api_version='v2', ssl=True, debug=False):
        """
        Initialize a new instance of GolemioClient.

        Args:
            api_key (str): The API key (optional, default is an empty string).
            api_version (str): The API version to use (optional, default is 'v2').
            ssl (bool): Flag indicating whether to use SSL (optional, default is True).
            debug (bool): Flag indicating whether to use the debug mode (optional, default is False).
        """
        self.session = requests.Session()
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = 'rabin.golemio.cz' if debug else 'api.golemio.cz'
        self.protocol = 'https' if ssl else 'http'
        self.updateApiKey(api_key)

    def __del__(self):
        """
        Clean up resources by closing the session.
        """
        self.session.close()

    def _getUrl(self, path, params={}):
        """
        Construct the URL for the API request.

        Args:
            path (str): The API path.
            params (dict): Query parameters (optional, default is an empty dictionary).

        Returns:
            str: The constructed URL.
        """
        for param in params:
            if isinstance(params[param], bool):
                params[param] = str(params[param]).lower()
        query = '?' + urllib.parse.urlencode(params, doseq=True)
        url = f'{self.protocol}://{self.base_url}/{self.api_version}{path}{query}'
        return url

    def _callApi(self, path, proto=False, params={}):
        """
        Make the API request and handle common error responses.

        Args:
            path (str): The API path.
            proto (bool): Flag indicating whether to retrieve the response as a binary protobuf (optional, default is False).
            params (dict): Query parameters (optional, default is an empty dictionary).

        Returns:
            dict or bytes: The response data, either as JSON or binary protobuf.

        Raises:
            UnauthorizedError: If the API key is invalid or missing (HTTP status code 401).
            NotFoundError: If the requested resource was not found (HTTP status code 404).
        """
        response = self.session.get(self._getUrl(path, params))
        if response.status_code == 401:
            raise UnauthorizedError(
                'Unauthorized: API key is invalid or missing.')
        elif response.status_code == 404:
            raise NotFoundError(
                'Not Found: The requested resource was not found.')
        if proto:
            return response.content
        return response.json()

    def updateApiKey(self, api_key):
        """
        Update the API key used for requests.

        Args:
            api_key (str): The new API key.
        """
        self.session.headers.update({
            'X-Access-Token': api_key
        })

    def getServices(self, date=None, limit=10, offset=0):
        """
        Retrieve the list of services.

        Args:
            date (str): The date for which to retrieve the services (optional, default is None).
            limit (int): The maximum number of services to retrieve (optional, default is 10).
            offset (int): The offset for pagination (optional, default is 0).

        Returns:
            list: A list of services.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
            NotFoundError: If the requested resource was not found.
        """
        path = '/gtfs/services'
        params = {'limit': limit, 'offset': offset}
        if date:
            params['date'] = date
        return self._callApi(path, params=params)

    def getRoute(self, route_id):
        """
        Retrieve information about a specific route.

        Args:
            route_id (str): The ID of the route.

        Returns:
            dict: Information about the route.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
            NotFoundError: If the requested resource was not found.
        """
        path = f'/gtfs/routes/{route_id}'
        return self._callApi(path)

    def getTrips(self, stop_id=None, date=None, limit=10, offset=0):
        """
        Retrieve the list of trips.

        Args:
            stop_id (str): The ID of the stop to filter trips by (optional, default is None).
            date (str): The date for which to retrieve the trips (optional, default is None).
            limit (int): The maximum number of trips to retrieve (optional, default is 10).
            offset (int): The offset for pagination (optional, default is 0).

        Returns:
            list: A list of trips.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
            NotFoundError: If the requested resource was not found.
        """
        path = '/gtfs/trips'
        params = {'limit': limit, 'offset': offset}
        if stop_id:
            params['stopId'] = stop_id
        if date:
            params['date'] = date
        return self._callApi(path, params=params)

    def getShape(self, shape_id):
        """
        Retrieve information about a specific shape.

        Args:
            shape_id (str): The ID of the shape.

        Returns:
            dict: Information about the shape.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
            NotFoundError: If the requested resource was not found.
        """
        path = f'/gtfs/shapes/{shape_id}'
        return self._callApi(path)

    def getAllStops(self, names=None, stop_ids=None, asw_ids=None, cis_ids=None, limit=10000, offset=0):
        """
        Retrieve the list of all stops.

        Args:
            names (str or list): The names of stops to retrieve (optional, default is None).
            stop_ids (str or list): The IDs of stops to retrieve (optional, default is None).
            asw_ids (str or list): The ASW IDs of stops to retrieve (optional, default is None).
            cis_ids (str or list): The CIS IDs of stops to retrieve (optional, default is None).
            limit (int): The maximum number of stops to retrieve (optional, default is 10000).
            offset (int): The offset for pagination (optional, default is 0).

        Returns:
            list: A list of stops.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
        """
        path = '/gtfs/stops'
        params = {'limit': limit, 'offset': offset}
        if names:
            params['names'] = names
        if stop_ids:
            params['ids'] = stop_ids
        if asw_ids:
            params['aswIds'] = asw_ids
        if cis_ids:
            params['cisIds'] = cis_ids
        return self._callApi(path, params=params)

    def getStop(self, stop_id):
        """
        Retrieve information about a specific stop.

        Args:
            stop_id (str): The ID of the stop.

        Returns:
            dict: Information about the stop.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
            NotFoundError: If the requested resource was not found.
        """
        path = f'/gtfs/stops/{stop_id}'
        return self._callApi(path)

    def getStopTimes(self, stop_id, date=None, time_from=None, time_to=None, include_stop=False, limit=10000, offset=0):
        """
        Retrieve the list of stop times for a specific stop.

        Args:
            stop_id (str): The ID of the stop.
            date (str): The date for which to retrieve the stop times (optional, default is None).
            time_from (str): The starting time for the time range (optional, default is None).
            time_to (str): The ending time for the time range (optional, default is None).
            include_stop (bool): Flag indicating whether to include stop information (optional, default is False).
            limit (int): The maximum number of stop times to retrieve (optional, default is 10000).
            offset (int): The offset for pagination (optional, default is 0).

        Returns:
            list: A list of stop times.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
        """
        path = f'/gtfs/stoptimes/{stop_id}'
        params = {
            'includeStop': include_stop,
            'limit': limit,
            'offset': offset
        }
        if date:
            params['date'] = date
        if time_from:
            params['timeFrom'] = time_from
        if time_to:
            params['timeTo'] = time_to
        return self._callApi(path, params=params)

    def getAllVehiclePositions(self, limit=10000, offset=0, include_not_tracking=False, include_not_public=False,
                               include_positions=False, cis_trip_number=None, preferred_timezone=None, route_id=None,
                               route_short_name=None, updated_since=None):
        """
        Retrieve the list of all vehicle positions.

        Args:
            limit (int): The maximum number of vehicle positions to retrieve (optional, default is 10000).
            offset (int): The offset for pagination (optional, default is 0).
            include_not_tracking (bool): Flag indicating whether to include not tracking vehicles (optional, default is False).
            include_not_public (bool): Flag indicating whether to include not public vehicles (optional, default is False).
            include_positions (bool): Flag indicating whether to include vehicle positions (optional, default is False).
            cis_trip_number (str): The CIS trip number to filter vehicle positions by (optional, default is None).
            preferred_timezone (str): The preferred timezone for the results (optional, default is None).
            route_id (str): The ID of the route to filter vehicle positions by (optional, default is None).
            route_short_name (str): The short name of the route to filter vehicle positions by (optional, default is None).
            updated_since (str): The date and time since when the vehicle positions were updated (optional, default is None).

        Returns:
            list: A list of vehicle positions.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
        """
        path = '/vehiclepositions'
        params = {
            'limit': limit,
            'offset': offset,
            'includeNotTracking': include_not_tracking,
            'includeNotPublic': include_not_public,
            'includePositions': include_positions,
        }
        if cis_trip_number:
            params['cisTripNumber'] = cis_trip_number
        if preferred_timezone:
            params['preferredTimezone'] = preferred_timezone
        if route_id:
            params['routeId'] = route_id
        if route_short_name:
            params['routeShortName'] = route_short_name
        if updated_since:
            params['updatedSince'] = updated_since
        return self._callApi(path, params=params)

    def getDepartureBoards(self, ids=None, asw_ids=None, cis_ids=None, names=None, minutes_before=None,
                           minutes_after=180, time_from=None, include_metro_trains=False, air_condition=True,
                           preferred_timezone='Europe/Prague', mode='departures', order='real', filter=None,
                           skip=None, limit=20, total=None, offset=0):
        """
        Retrieve the departure boards for multiple stops.

        Args:
            ids (str or list): The IDs of the stops to retrieve departure boards for (optional, default is None).
            asw_ids (str or list): The ASW IDs of the stops to retrieve departure boards for (optional, default is None).
            cis_ids (str or list): The CIS IDs of the stops to retrieve departure boards for (optional, default is None).
            names (str or list): The names of the stops to retrieve departure boards for (optional, default is None).
            minutes_before (int): The number of minutes to include departures before the current time (optional, default is None).
            minutes_after (int): The number of minutes to include departures after the current time (optional, default is 180).
            time_from (str): The starting time for the time range (optional, default is None).
            include_metro_trains (bool): Flag indicating whether to include metro trains (optional, default is False).
            air_condition (bool): Flag indicating whether to include only vehicles with air conditioning (optional, default is True).
            preferred_timezone (str): The preferred timezone for the results (optional, default is 'Europe/Prague').
            mode (str): The mode of departure boards to retrieve (optional, default is 'departures').
            order (str): The order of departures (optional, default is 'real').
            filter (str): The filter for departures (optional, default is None).
            skip (int): The number of departures to skip (optional, default is None).
            limit (int): The maximum number of departures to retrieve (optional, default is 20).
            total (int): The total number of departures (optional, default is None).
            offset (int): The offset for pagination (optional, default is 0).

        Returns:
            list: A list of departure boards.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
        """
        path = '/pid/departureboards'
        params = {
            'limit': limit,
            'offset': offset
        }
        if ids is not None:
            params['ids'] = ids
        if asw_ids is not None:
            params['aswIds'] = asw_ids
        if cis_ids is not None:
            params['cisIds'] = cis_ids
        if names is not None:
            params['names'] = names
        if minutes_before is not None:
            params['minutesBefore'] = minutes_before
        params['minutesAfter'] = minutes_after
        if time_from is not None:
            params['timeFrom'] = time_from
        params['includeMetroTrains'] = include_metro_trains
        params['airCondition'] = air_condition
        params['preferredTimezone'] = preferred_timezone
        params['mode'] = mode
        params['order'] = order
        if filter is not None:
            params['filter'] = filter
        if skip is not None:
            params['skip'] = skip
        if total is not None:
            params['total'] = total
        return self._callApi(path, params=params)

    def getInfoTexts(self):
        """
        Retrieve the information texts.

        Returns:
            list: A list of information texts.

        Raises:
            UnauthorizedError: If the API key is invalid or missing.
        """
        path = '/pid/infotexts'
        return self._callApi(path)
