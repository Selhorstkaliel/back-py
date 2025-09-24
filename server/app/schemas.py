from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, Literal, List
from datetime import datetime
from decimal import Decimal

class UserBase(BaseModel):
    name: str
    email: EmailStr
    username: str
    role: Literal["admin", "representante", "vendedor"]
    phone: Optional[str]

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RepresentativeOut(BaseModel):
    user_id: int
    default_discount: Decimal

class SellerOut(BaseModel):
    user_id: int
    representative_id: int
    seller_discount: Decimal

class EntryBase(BaseModel):
    tipo: Literal["limpeza", "rating"]
    doc: str
    nome: str
    telefone: str
    vendedor: str
    valor: Decimal
    desconto: Decimal
    liquido: Decimal
    status: Literal["Restrição", "Finalizado", "Reprotocolo"]
    feito: bool

class EntryCreate(BaseModel):
    tipo: Literal["limpeza", "rating"]
    doc: str
    nome: str
    telefone: str
    vendedor: str
    valor: Decimal
    desconto: Optional[Decimal]
    aceitoTermos: bool

class EntryOut(EntryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int

    class Config:
        from_attributes = True

class TicketOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    created_at: datetime

class FileOut(BaseModel):
    id: int
    path: str
    mime: str
    entry_id: Optional[int]
    ticket_id: Optional[int]