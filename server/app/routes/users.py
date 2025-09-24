from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import User, RoleEnum, Representative, Seller
from ..schemas import UserCreate, UserOut
from ..deps import get_db, get_logged_in_user

router = APIRouter()

# Exemplo: CRUD de representantes (admin)
@router.get("/representantes", response_model=list[UserOut])
def list_representantes(db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    if user["role"] != "admin":
        raise HTTPException(403)
    reps = db.query(User).filter(User.role == RoleEnum.representante).all()
    return reps

@router.post("/representantes", response_model=UserOut)
def create_representante(data: UserCreate, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    if user["role"] != "admin":
        raise HTTPException(403)
    exists = db.query(User).filter((User.email == data.email) | (User.username == data.username)).first()
    if exists:
        raise HTTPException(400, "Usuário já existe")
    u = User(
        name=data.name, email=data.email, username=data.username,
        role=RoleEnum.representante, password_hash=hash_password(data.password)
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    rep = Representative(user_id=u.id, default_discount=0)
    db.add(rep)
    db.commit()
    return u

# Similar para PATCH/DELETE (adicione conforme necessário)