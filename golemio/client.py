import requests
import urllib.parse


class GolemioClient(object):

    def __init__(self, api_key, api_version='v2', ssl=True, debug=False):
        self.session = requests.Session()
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = 'rabin.golemio.cz' if debug else 'api.golemio.cz'
        self.protocol = 'https' if ssl else 'http'
        self.updateApiKey(api_key)

    def _getUrl(self, path, params={}):
        # Current API have a bug
        # Requests with boolean values in query which is in lower case
        # Will not work
        # Example :
        # Working Request
        # https://rabin.golemio.cz/v2/gtfs/trips/991_5735_230703?includeShapes=false&includeStops=false&includeStopTimes=false&includeService=false&includeRoute=false
        # https://rabin.golemio.cz/v2/gtfs/trips/991_5735_230703?includeShapes=false&includeStops=False&includeStopTimes=False&includeService=False&includeRoute=False
        # TODO Commit this bug to golemio and delete this FIX
        ############################################
        for param in params:
            if type(params[param]) is bool:
                params[param] = str(params[param]).lower()
        ############################################
        query = '?' + urllib.parse.urlencode(params, doseq=True)
        url = f'{self.protocol}://{self.base_url}/{self.api_version}{path}{query}'
        return url

    def _callApi(self, path, proto=False, params={}):
        response = self.session.get(self._getUrl(path, params))
        response.raise_for_status()
        if proto:
            return response.content
        return response.json()

    def updateApiKey(self, api_key):
        self.session.headers.update({
            'X-Access-Token': api_key
        })

    def getServices(self, date=None, limit=10, offset=0):
        path = '/gtfs/services'
        params = {'limit': limit,
                  'offset': offset}
        if date:
            params['date'] = date
        return self._callApi(path, params=params)

    def getRoutes(self, offset=0, limit=10):
        path = '/gtfs/routes'
        params = {'offset': offset,
                  'limit': limit}
        return self._callApi(path, params=params)

    def getRoute(self, route_id):
        path = f'/gtfs/routes/{route_id}'
        return self._callApi(path)

    def getTrips(self, stop_id=None, date=None, limit=10, offset=0):
        path = '/gtfs/trips'
        params = {'limit': limit,
                  'offset': offset}
        if stop_id:
            params['stopId'] = stop_id
        if date:
            params['date'] = date
        return self._callApi(path, params=params)

    def getTrip(self, trip_id, include_shapes=False, include_stops=False, include_stop_times=False, include_service=False, include_route=False, date=None):
        path = f'/gtfs/trips/{trip_id}'
        params = {
            'includeShapes': include_shapes,
            'includeStops': include_stops,
            'includeStopTimes': include_stop_times,
            'includeService': include_service,
            'includeRoute': include_route,
        }
        if date:
            params['date'] = date

        return self._callApi(path, params=params)

    def getShape(self, shape_id):
        path = f'/gtfs/shapes/{shape_id}'
        return self._callApi(path)

    def getAllStops(self, names=None, stop_ids=None, asw_ids=None, cis_ids=None, limit=10000, offset=0):
        path = '/gtfs/stops'
        params = {
            'limit': limit,
            'offset': offset
        }
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
        path = f'/gtfs/stops/{stop_id}'
        return self._callApi(path)

    def getStopTimes(self, stop_id, date=None, time_from=None, time_to=None, include_stop=False, limit=10000, offset=0):
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

    def protoTripUpdates(self):
        path = '/vehiclepositions/gtfsrt/trip_updates.pb'
        return self._callApi(path, proto=True)

    def protoVehiclePosUpdates(self):
        path = '/vehiclepositions/gtfsrt/vehicle_positions.pb'
        return self._callApi(path, proto=True)

    def protoPidFeed(self):
        path = '/vehiclepositions/gtfsrt/pid_feed.pb'
        return self._callApi(path, proto=True)

    def protoServiceAlerts(self):
        path = '/vehiclepositions/gtfsrt/alerts.pb'
        return self.callApi(path, proto=True)

    def getAllVehiclePositions(self, limit=10000, offset=0, include_not_tracking=False, include_not_public=False, include_positions=False, cis_trip_number=None, preferred_timezone=None, route_id=None, route_short_name=None, updated_since=None):
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

    def getDepartureBoards(self, ids=None, asw_ids=None, cis_ids=None, names=None, minutes_before=None, minutes_after=180, time_from=None, include_metro_trains=False, air_condition=True, preferred_timezone='Europe/Prague', mode='departures', order='real', filter=None, skip=None, limit=20, total=None, offset=0):
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
        path = '/pid/infotexts'
        return self._callApi(path)
