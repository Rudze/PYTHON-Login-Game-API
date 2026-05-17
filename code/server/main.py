import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import asyncio
import websockets
from jwt_verify import get_user_from_token
from player import Player
from game_loop import on_player_connect, on_player_disconnect, handle_message
from config import HOST, PORT


async def handle_connection(websocket):
    # Première chose : le client envoie son token
    token = await websocket.recv()

    user = get_user_from_token(token)
    if user is None:
        await websocket.send('{"type": "error", "message": "Token invalide"}')
        await websocket.close()
        return

    player = Player(
        user_id=user["user_id"],
        username=user["username"],
        websocket=websocket
    )
    await on_player_connect(player)

    try:
        async for message in websocket:
            await handle_message(player, message)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        await on_player_disconnect(player)


async def main():
    print(f"Server démarré sur {HOST}:{PORT}")
    async with websockets.serve(handle_connection, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())