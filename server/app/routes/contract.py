from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..models import Entry
from ..deps import get_db, get_logged_in_user
from ..services.contract import gerar_contrato_pdf

router = APIRouter()

@router.get("/{entry_id}")
def download_contract(entry_id: int, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(404)
    path = f"./data/contracts/{entry_id}.pdf"
    if not os.path.exists(path):
        raise HTTPException(404)
    return FileResponse(path, media_type="application/pdf", filename=f"contrato_{entry_id}.pdf")