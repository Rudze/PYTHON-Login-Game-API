import json
import websockets


class Player:
    def __init__(self, user_id: int, username: str, websocket):
        self.user_id   = user_id
        self.username  = username
        self.websocket = websocket

        # Position sur la map
        self.x   = 0
        self.y   = 0
        self.map = "spawn"

        # État
        self.is_alive = True
        self.hp       = 100
        self.max_hp   = 100

    async def send(self, data: dict):
        try:
            await self.websocket.send(json.dumps(data))
        except Exception:
            pass

    def __repr__(self):
        return f"Player({self.user_id}, {self.username}, {self.map})"