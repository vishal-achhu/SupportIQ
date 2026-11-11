import os, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from .models import User

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("JWT_SECRET", "replace-with-a-random-secret-of-at-least-32-characters")

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)

def make_token(user: User) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", "60")))
    return jwt.encode({"sub": str(user.id), "exp": expiry}, SECRET, algorithm="HS256")

def current_user(authorization: str | None = Header(default=None), db: Session = None) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Bearer token required")
    try:
        payload = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
    user = db.get(User, user_id) if db else None
    if not user:
        raise HTTPException(401, "User not found")
    return user
