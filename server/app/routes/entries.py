from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..models import Entry, EntryStatusEnum, User
from ..schemas import EntryCreate, EntryOut
from ..deps import get_db, get_logged_in_user
from ..services.discounts import calcular_desconto_efetivo

router = APIRouter()

@router.post("/", response_model=EntryOut)
async def create_entry(
    tipo: str = Form(...),
    doc: str = Form(...),
    nome: str = Form(...),
    telefone: str = Form(...),
    vendedor: str = Form(...),
    valor: float = Form(...),
    aceitoTermos: bool = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_logged_in_user)
):
    if not aceitoTermos:
        raise HTTPException(400, "Aceite os termos para gerar contrato")
    desconto = calcular_desconto_efetivo(db, user)
    liquido = max(0, float(valor) - float(desconto))
    entry = Entry(
        tipo=tipo, doc=doc, nome=nome, telefone=telefone, vendedor=vendedor,
        valor=valor, desconto=desconto, liquido=liquido,
        status=EntryStatusEnum.Restricao, feito=False, created_by=user["id"]
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    # Salvar arquivo, gerar contrato PDF etc (ponto de extensão)
    return entry

@router.get("/", response_model=list[EntryOut])
def list_entries(limit: int = 50, page: int = 1, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    q = db.query(Entry)
    # RBAC: admin vê tudo, representante vê próprios e vendedores, vendedor só seus
    # Implemente os filtros conforme papel
    entries = q.limit(limit).offset((page-1)*limit).all()
    return entries

@router.patch("/{id}/status")
def patch_status(id: int, status: str, db: Session = Depends(get_db), user=Depends(get_logged_in_user)):
    if user["role"] != "admin":
        raise HTTPException(403)
    entry = db.query(Entry).filter(Entry.id == id).first()
    if not entry:
        raise HTTPException(404)
    entry.status = status
    db.commit()
    return {"ok": True}