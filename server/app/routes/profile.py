from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_logged_in_user
from ..schemas import UserOut

router = APIRouter()

@router.get("/", response_model=UserOut)
def get_profile(db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    u = db.query(User).filter(User.id == user["id"]).first()
    return u

@router.patch("/")
def update_profile(data: dict, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    u = db.query(User).filter(User.id == user["id"]).first()
    for k, v in data.items():
        setattr(u, k, v)
    db.commit()
    return {"ok": True}