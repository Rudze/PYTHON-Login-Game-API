"""
Ce fichier gère l'authentification utilisateur.

- register() : crée un compte utilisateur (signup)
- login()    : connecte un utilisateur et génère un JWT

Il utilise :
- MySQL (via pymysql)
- bcrypt (hash sécurisé des mots de passe)
- JWT (tokens de session)
- logger (affichage console pour debug)
"""

import bcrypt
from database import get_connection
from shared.tools.logger import log_error, log_success
from jwt_handler import create_token


def register(username: str, email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Vérifie si le username ou email existe déjà
        cursor.execute(
            "SELECT id FROM users WHERE username = %s OR email = %s",
            (username, email)
        )

        if cursor.fetchone():
            log_error("Nom d'utilisateur ou email déjà utilisé")
            return {"success": False, "error": "Utilisateur déjà existant"}

        # Hash sécurisé du mot de passe (bcrypt)
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Insère le nouvel utilisateur en base
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )

        conn.commit()
        log_success("Compte créé avec succès")

        return {"success": True}

    except Exception as e:
        # Annule les changements si erreur serveur
        conn.rollback()
        log_error(f"Erreur serveur: {e}")
        return {"success": False, "error": "Erreur serveur"}

    finally:
        # Nettoyage des ressources DB
        cursor.close()
        conn.close()


def login(username: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Récupère l'utilisateur par username
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,)
        )

        user = cursor.fetchone()

        # Si utilisateur introuvable
        if not user:
            log_error("Identifiants incorrects")
            return {"success": False, "error": "Identifiants incorrects"}

        # Vérifie le mot de passe avec bcrypt
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):
            log_error("Identifiants incorrects")
            return {"success": False, "error": "Identifiants incorrects"}

        # Génère un token JWT si login OK
        token = create_token(user["id"], user["username"])

        return {
            "success": True,
            "token": token
        }

    except Exception as e:
        # Erreur inattendue (DB, code, etc.)
        return {"success": False, "error": str(e)}

    finally:
        # Fermeture propre de la connexion DB
        cursor.close()
        conn.close()