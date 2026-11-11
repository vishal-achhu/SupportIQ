from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
import jwt, os
from .db import get_db
from .models import User

def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        payload = jwt.decode(authorization[7:], os.getenv("JWT_SECRET", "replace-with-a-random-secret-of-at-least-32-characters"), algorithms=["HS256"])
        uid = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get(User, uid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
