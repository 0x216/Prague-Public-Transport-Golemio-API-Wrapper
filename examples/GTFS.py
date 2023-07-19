from golemio.client import GolemioClient

# Create a GolemioClient instance
client = GolemioClient(api_key='YOUR_API_KEY')

# Retrieve a list of services
services = client.getGTFSServices()

# Print the service information
for service in services:
    print(f"Service ID: {service['service_id']}")

# Retrieve a list of routes
routes = client.getGTFSRoutes()
for route in routes:
    print(f"Route ID: {route['route_id']}")
