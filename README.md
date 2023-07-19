
# Golemio Python Client

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/your_username/golemio-python-client/blob/main/LICENSE)

The Golemio Python Client is a Python wrapper for the Golemio API, providing easy access to public transportation data and GTFS (General Transit Feed Specification) information. With this client, you can retrieve data about services, routes, stops, trips, vehicle positions, departure boards, and more.

## Key Features

- Retrieve information about public transportation services, routes, stops, and trips.
- Access GTFS static data such as route details, stop information, and shapes.
- Retrieve GTFS Realtime data including vehicle positions, trip updates, and service alerts.
- Get departure boards for multiple stops to obtain real-time departure information.
- Simple and intuitive interface for seamless integration with your projects.

## Installation

You can install the Golemio Python Client using pip:

```bash
pip install golemic-pid-api==0.1
```
## Usage

To get started with the Golemio Python Client, follow these steps:

1. Import the `GolemioClient` class:

```python
from golemio.client import GolemioClient
```

2. Create an instance of the `GolemioClient` class:

```python
client = GolemioClient(api_key='YOUR_API_KEY')
```

3. Retrieve public transportation data:

```python
# Get the list of services
services = client.getServices()

# Get information about a specific route
route_id = 'ROUTE_ID'
route = client.getRoute(route_id)

# Get the list of trips
trips = client.getTrips(stop_id='STOP_ID')

# Get information about a specific shape
shape_id = 'SHAPE_ID'
shape = client.getShape(shape_id)

# Get information about all stops
stops = client.getAllStops()

# Get information about a specific stop
stop_id = 'STOP_ID'
stop = client.getStop(stop_id)

# Get the list of stop times for a specific stop
stop_id = 'STOP_ID'
stop_times = client.getStopTimes(stop_id)

# Get the list of all vehicle positions
vehicle_positions = client.getAllVehiclePositions()

# Get departure boards for multiple stops
departure_boards = client.getDepartureBoards(ids=['STOP1', 'STOP2'])

# Get the information texts
info_texts = client.getInfoTexts()

# Retrieve the GTFS Realtime feeds
trip_updates = client.getTripUpdatesProtobuf()
vehicle_positions = client.getVehiclePositionsProtobuf()
pid_feed = client.getPidFeedProtobuf()
```

For more details on the available methods and their parameters, please refer to the [Golemio API Documentation](https://api.golemio.cz/v2/pid/docs/openapi/#/).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/your_username/golemio-python-client/blob/main/LICENSE) file for details.
