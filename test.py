import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as ws:
        print("Connected to matchmaker server!")
        try:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                print("Received:", json.dumps(data, indent=2))
        except websockets.ConnectionClosed:
            print("Connection closed by server")

asyncio.run(test_client())