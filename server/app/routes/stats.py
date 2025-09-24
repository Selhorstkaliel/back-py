from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_logged_in_user

router = APIRouter()

@router.get("/")
def stats(db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    # Exemplo: KPIs
    bruto = db.execute("SELECT SUM(valor) FROM entries").scalar() or 0
    liquido = db.execute("SELECT SUM(liquido) FROM entries").scalar() or 0
    limpezas = db.execute("SELECT COUNT(*) FROM entries WHERE tipo='limpeza'").scalar() or 0
    ratings = db.execute("SELECT COUNT(*) FROM entries WHERE tipo='rating'").scalar() or 0
    return {
        "bruto": bruto, "liquido": liquido, "limpezasCount": limpezas, "ratingCount": ratings
    }