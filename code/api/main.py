"""
API principale du backend.

Cette API permet :
- l'inscription utilisateur
- la connexion utilisateur
- la récupération d'un serveur disponible

Elle utilise :
- FastAPI (API web)
- JWT (authentification)
- MySQL (base de données)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

from auth import register, login
from jwt_handler import verify_token
from database import get_connection, init_db


# Création de l'application FastAPI
app = FastAPI()

# Exécuté automatiquement au démarrage du serveur
@app.on_event("startup")
def startup():
    # Initialise les tables SQL
    init_db()

# Format attendu pour /register
class RegisterBody(BaseModel):
    username: str
    email: str
    password: str

# Format attendu pour /login
class LoginBody(BaseModel):
    username: str
    password: str

# Route POST /register
@app.post("/register")
def route_register(body: RegisterBody):
    # Appelle la logique d'inscription
    result = register(
        body.username,
        body.email,
        body.password
    )
    # Si erreur → renvoie HTTP 400
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )
    # Retour succès
    return result

# Route POST /login
@app.post("/login")
def route_login(body: LoginBody):
    # Appelle la logique de connexion
    result = login(
        body.username,
        body.password
    )
    # Si erreur → non autorisé
    if not result["success"]:
        raise HTTPException(
            status_code=401,
            detail=result["error"]
        )
    return result

# Route GET protégée par JWT
@app.get("/server-info")
def route_server_info(
    # Récupère le header Authorization
    authorization: str = Header(...)
):

    # Sépare "Bearer TOKEN"
    token_parts = authorization.split(" ")

    # Vérifie le format du header
    if len(token_parts) != 2 or token_parts[0] != "Bearer":

        raise HTTPException(
            status_code=401,
            detail="Format token invalide"
        )

    # Vérifie le token JWT
    payload = verify_token(token_parts[1])

    # Si token invalide ou expiré
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré"
        )

    # Connexion base de données
    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Cherche un serveur disponible
        cursor.execute("""
            SELECT
                name,
                ip,
                port,
                region,
                current_players,
                max_players
            FROM servers
            WHERE is_online = TRUE
            ORDER BY current_players ASC
            LIMIT 1
        """)

        # Récupère le premier serveur trouvé
        server = cursor.fetchone()

        # Aucun serveur trouvé
        if not server:

            raise HTTPException(
                status_code=503,
                detail="Aucun serveur disponible"
            )

        # Retourne les infos serveur
        return {
            "success": True,
            "server": server
        }

    finally:

        # Fermeture propre de la DB
        cursor.close()
        conn.close()