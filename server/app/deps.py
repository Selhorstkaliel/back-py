from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from .db import SessionLocal
from .security import get_current_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_logged_in_user(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user