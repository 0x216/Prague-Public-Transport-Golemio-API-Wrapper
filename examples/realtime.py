from golemio.client import GolemioClient

# Create a GolemioClient instance
client = GolemioClient(api_key='YOUR_API_KEY', debug=True)

# Retrieve a list of services
veh_positions = client.getAllVehiclePositions()

for veh in veh_positions['features']:
    print(veh['geometry']['coordinates'])
