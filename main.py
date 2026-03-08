import asyncio
import websockets
import json
import time
import hashlib
from colorama import init, Fore
## colorama for colors and shi

init(autoreset=True)

async def handler(websocket, path):
    if "xmpp" in websocket.request_headers.get("Sec-Websocket-Protocol", "").lower():
        await websocket.close()
        return

    ticket_id = hashlib.md5(f"1{int(time.time() * 1000)}".encode()).hexdigest() 
    match_id = hashlib.md5(f"2{int(time.time() * 1000)}".encode()).hexdigest()
    session_id = hashlib.md5(f"3{int(time.time() * 1000)}".encode()).hexdigest()

    await asyncio.sleep(0.8)
    await send_status(websocket, "Waiting", total_players=1, connected_players=1)
    await asyncio.sleep(0.8)
    await send_status(websocket, "Queued", ticket_id=ticket_id, Queued_players=0, estimated_wait_sec=0)
    await asyncio.sleep(0.8)
    await send_status(websocket, "SessionAssignment", match_id=match_id)
    await asyncio.sleep(4)

    await send_play(websocket, match_id, session_id)

async def send_status(websocket, state, **kwargs):
    message = {
        "payload": {"state": state, **kwargs},
        "name": "StatusUpdate"
    }
    await websocket.send(json.dumps(message))

async def send_play(websocket, match_id, session_id):
    message = {
        "payload": {
            "MatchId": match_id,
            "sessionId": session_id,
            "joinDelaySec": 0,
        },
        "name": "Play"
    }
    await websocket.send(json.dumps(message))

async def main():
    port = 8080
    server = await websockets.serve(handler, "0.0.0.0", port)
    print(Fore.GREEN + f"MatchmakerPY started listening on {port}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())