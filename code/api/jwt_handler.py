"""
Ce fichier gère les tokens JWT utilisés pour l'authentification.

- create_token() : crée un token JWT pour un utilisateur
- verify_token() : vérifie qu'un token est valide

Les tokens JWT servent souvent à :
- garder un utilisateur connecté
- sécuriser une API
- identifier un joueur connecté
"""

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from config import JWT_SECRET, JWT_EXPIRE_SECONDS


# Algorithme utilisé pour signer le token
ALGORITHM = "HS256"


def create_token(user_id: int, username: str) -> str:

    # Date d'expiration du token
    expire = datetime.now(timezone.utc) + timedelta(
        seconds=JWT_EXPIRE_SECONDS
    )

    # Données stockées dans le token
    payload = {
        "sub": str(user_id),   # ID utilisateur
        "username": username,  # Nom utilisateur
        "exp": expire          # Expiration du token
    }

    # Génère et retourne le token JWT signé
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM
    )


def verify_token(token: str) -> dict | None:
    try:
        # Vérifie et décode le token
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        # Token invalide ou expiré
        return None