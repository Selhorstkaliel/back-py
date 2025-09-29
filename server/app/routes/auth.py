from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from ..db import SessionLocal
from ..models import User, RoleEnum
from ..schemas import UserOut
from ..security import (
    hash_password, verify_password, create_jwt, get_current_user
)
from ..deps import get_db

router = APIRouter()

@router.post("/login")
def login(request: Request, response: Response, username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt({"sub": user.username, "role": user.role.value, "id": user.id, "name": user.name, "email": user.email})
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        secure=settings.NODE_ENV == "production",
        samesite="lax",
        max_age=60 * 60 * 8,
    )
    return {
        "id": user.id, "name": user.name, "email": user.email, "role": user.role.value
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="jwt",
        httponly=True,
        secure=settings.NODE_ENV == "production",
        samesite="lax",
    )
    return {"ok": True}

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user["id"]).first()
    if not u:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return u
