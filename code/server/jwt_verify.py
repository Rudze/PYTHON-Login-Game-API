from jose import jwt, JWTError
from config import JWT_SECRET, ALGORITHM

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_from_token(token: str) -> dict | None:
    payload = verify_token(token)
    if payload is None:
        return None

    return {
        "user_id": int(payload.get("sub")),
        "username": payload.get("username")
    }