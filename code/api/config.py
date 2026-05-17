from dotenv import load_dotenv
import os

# Charge automatiquement le fichier .env
load_dotenv()


# Récupère les variables d'environnement
DB_HOST             = os.getenv("DB_HOST")
DB_PORT             = int(os.getenv("DB_PORT"))
DB_USER             = os.getenv("DB_USER")
DB_PASSWORD         = os.getenv("DB_PASSWORD")
DB_NAME             = os.getenv("DB_NAME")

JWT_SECRET          = os.getenv("JWT_SECRET")
JWT_EXPIRE_SECONDS  = int(os.getenv("JWT_EXPIRE_SECONDS"))


#
required_vars = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
    "JWT_SECRET": JWT_SECRET,
    "JWT_EXPIRE_SECONDS": JWT_EXPIRE_SECONDS,
}

# Liste des variables manquantes
#
# On parcourt le dictionnaire avec .items()
# Si value est vide ou None :
# alors on ajoute le nom dans la liste
missing_vars = [
    name
    for name, value in required_vars.items()
    if not value
]

# Si la liste n'est pas vide :
# alors il manque des variables
if missing_vars:
    raise ValueError(
        f"Variables d'environnement manquantes : {', '.join(missing_vars)}"
    )