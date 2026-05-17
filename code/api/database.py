"""
Ce fichier gère la connexion MySQL et l'initialisation de la base de données.

- get_connection() : ouvre une connexion à MySQL
- init_db()        : crée les tables nécessaires si elles n'existent pas
"""

import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    # Ouvre une connexion MySQL
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,

        # Retourne les résultats SQL sous forme de dictionnaires
        cursorclass=pymysql.cursors.DictCursor
    )


def init_db():

    # Connexion à la base de données
    conn = get_connection()

    # Curseur permettant d'exécuter des requêtes SQL
    cursor = conn.cursor()

    # Création de la table des utilisateurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            username      VARCHAR(50)  NOT NULL UNIQUE,
            email         VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Création de la table des serveurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            name            VARCHAR(100) NOT NULL,
            ip              VARCHAR(45)  NOT NULL,
            port            INT          NOT NULL,
            region          VARCHAR(50),
            is_online       BOOLEAN DEFAULT FALSE,
            max_players     INT DEFAULT 100,
            current_players INT DEFAULT 0,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sauvegarde les changements dans la base
    conn.commit()

    # Ferme le curseur
    cursor.close()

    # Ferme la connexion MySQL
    conn.close()
