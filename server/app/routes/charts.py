from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_logged_in_user

router = APIRouter()

@router.get("/vendas")
def vendas(year: int, month: int, half: int, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    # Exemplo: Pega vendas por quinzena
    # Implemente query real para labels + counts
    return {
        "labels": ["1-15", "16-30"],
        "counts": [5, 7]
    }

@router.get("/rating")
def rating(year: int, month: int, half: int, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    # Exemplo: rating feitos/não feitos por quinzena
    return {
        "feito": 3,
        "nao_feito": 2
    }