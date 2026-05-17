from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET  = os.getenv("JWT_SECRET")
ALGORITHM   = "HS256"

# Game server
HOST        = os.getenv("HOST")
PORT        = int(os.getenv("PORT"))

#
required_vars = {
    "HOST": HOST,
    "PORT": PORT,
    "JWT_SECRET": JWT_SECRET,
}

missing_vars = [
    name
    for name, value in required_vars.items()
    if not value
]

if missing_vars:
    raise ValueError(
        f"Variables d'environnement manquantes : {', '.join(missing_vars)}"
    )