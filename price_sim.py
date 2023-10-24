import asyncio
import websockets

import random
import requests


async def send_price_update():
    URI = 'ws://localhost:8765'

    async with websockets.connect(uri=URI) as websocket:
        while True: 
            sim_price = 25 + random.uniform(-5, 5)
            PUT_sim_price = f'{sim_price:.2f}'
            try:
                requests.put("http://127.0.0.1:5000/stock", 
                                       json= {
                                           "ticker": "NMRT",
                                           "price": float(PUT_sim_price)
                                       })
                print('Connected, The price for the stock "NMRT" has changed!')
            except Exception as e:
                print(f'Error making the put request! {e}')

            await websocket.send(f'-UPDATE- the price for the stock "NMRT" is now: {sim_price:.2f}')

            await asyncio.sleep(5)

asyncio.get_event_loop().run_until_complete(send_price_update())