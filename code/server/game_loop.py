import asyncio
import json
from player import Player
from shared.tools.logger import log_success, log_error, log_disconnect, log_connection

connected_players: dict[int, Player] = {}


async def on_player_connect(player: Player):
    connected_players[player.user_id] = player
    log_connection(f"{player.username} connecté ({len(connected_players)} joueurs en ligne)")

    await player.send({
        "type": "welcome",
        "message": f"Bienvenue {player.username} !",
        "position": {"x": player.x, "y": player.y, "map": player.map}
    })


async def on_player_disconnect(player: Player):
    connected_players.pop(player.user_id, None)
    log_connection(f"{player.username} disconnected ({len(connected_players)} joueurs en ligne)")

async def handle_message(player: Player, raw: str):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        await player.send({"type": "error", "message": "Message invalide"})
        return

    msg_type = data.get("type")

    if msg_type == "move":
        await handle_move(player, data)

    elif msg_type == "ping":
        await player.send({"type": "pong"})

    else:
        await player.send({"type": "error", "message": f"Type inconnu : {msg_type}"})


async def handle_move(player: Player, data: dict):
    x = data.get("x")
    y = data.get("y")

    if x is None or y is None:
        await player.send({"type": "error", "message": "Position manquante"})
        return

    player.x = x
    player.y = y

    await player.send({
        "type": "move_ok",
        "position": {"x": player.x, "y": player.y}
    })

    await broadcast_except(player, {
        "type": "player_moved",
        "user_id": player.user_id,
        "username": player.username,
        "position": {"x": player.x, "y": player.y}
    })


async def broadcast_except(sender: Player, data: dict):
    for player in connected_players.values():
        if player.user_id != sender.user_id and player.map == sender.map:
            await player.send(data)