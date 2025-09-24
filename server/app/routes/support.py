from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..models import Ticket, File as FileModel
from ..deps import get_db, get_logged_in_user

router = APIRouter()

@router.get("/")
def list_tickets(db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    tickets = db.query(Ticket).filter(Ticket.user_id == user["id"]).all()
    return tickets

@router.post("/")
async def open_ticket(title: str, description: str, file: UploadFile = File(None), db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    t = Ticket(user_id=user["id"], title=title, description=description)
    db.add(t)
    db.commit()
    db.refresh(t)
    # Salvar arquivo se houver
    if file:
        path = f"./data/files/ticket_{t.id}_{file.filename}"
        with open(path, "wb") as f:
            f.write(await file.read())
        fmodel = FileModel(path=path, mime=file.content_type, ticket_id=t.id)
        db.add(fmodel)
        db.commit()
    return t