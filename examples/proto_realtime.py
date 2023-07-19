from golemio.client import GolemioClient
# pip install protobuf
from google.transit import gtfs_realtime_pb2

# Create a GolemioClient instance
client = GolemioClient(api_key='YOUR_API_KEY', debug=True)

# Retrieve a list of services
veh_positions = client.getVehiclePositionsProtobuf()
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(veh_positions)
for entity in feed.entity:
    print(f'Entity ID {entity.id}')
    print(f'Trip ID {entity.vehicle.trip.trip_id}')
    print(f'Position {entity.vehicle.position}')
