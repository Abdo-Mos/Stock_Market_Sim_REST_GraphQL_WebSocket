import asyncio
import websockets

from datetime import datetime


async def handle_price_change_data(websockets, path):
    print('connected')
    try:
        async for message in websockets:
            print(f'Recieved Client Message: {message} Time: {datetime.now()}')
    except websockets.exceptions.ConnectionClosedOK:
        print(f'Connection closed by {websockets.remote_address}')
    except Exception as e:
        print(f'Error: {e}')

start_server = websockets.serve(handle_price_change_data, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()