import asyncio
import websockets
import httpx
import json

API_URL    = "http://localhost:8000"
SERVER_URL = "ws://localhost:5000"


async def main():
    # 1. Login sur l'API
    print("1. Login sur l'API...")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/login", json={
            "username": "test",
            "password": "monmotdepasse"
        })
        data = response.json()

    if not data.get("success"):
        print(f"Erreur login : {data.get('detail')}")
        return

    token = data["token"]
    print(f"   Token reçu : {token[:40]}...")

    # 2. Connexion WebSocket au game server
    print("2. Connexion au game server...")
    async with websockets.connect(SERVER_URL) as ws:

        # 3. Envoyer le token en premier
        await ws.send(token)
        print("   Token envoyé")

        # 4. Recevoir le message welcome
        welcome = json.loads(await ws.recv())
        print(f"   Serveur : {welcome}")

        # 5. Envoyer un mouvement
        print("3. Envoi d'un move...")
        await ws.send(json.dumps({
            "type": "move",
            "x": 10,
            "y": 5
        }))

        move_response = json.loads(await ws.recv())
        print(f"   Serveur : {move_response}")

        # 6. Ping / Pong
        print("4. Ping...")
        await ws.send(json.dumps({"type": "ping"}))
        pong = json.loads(await ws.recv())
        print(f"   Serveur : {pong}")

    print("\nTout fonctionne !")


if __name__ == "__main__":
    asyncio.run(main())