from aiohttp import web # framework for web in python
import asyncio
import os
import socket
from datetime import datetime

# Handle the requests
async def handle(request):
    name = request.match_info.get('name', os.getenv("NAME", "World"))
    data = {'Name': name, 'Host': socket.gethostname(), 'Path': os.getcwd(),
            'Timestamp': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    return web.json_response(data)

# Define the type of app as Web aplication
app = web.Application()

# Define the routes of the web application
app.add_routes([
    (web.get('/', handle)),
    web.get('/{name}', handle)
])

# Start the server by 8080 port
if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port=5000)
