from sqlalchemy import (
    Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey, Enum, Text
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class RoleEnum(enum.Enum):
    admin = "admin"
    representante = "representante"
    vendedor = "vendedor"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    representative = relationship("Representative", uselist=False, back_populates="user")
    seller = relationship("Seller", uselist=False, back_populates="user")

class Representative(Base):
    __tablename__ = "representatives"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    default_discount = Column(Numeric, default=0)
    user = relationship("User", back_populates="representative")
    sellers = relationship("Seller", back_populates="representative")

class Seller(Base):
    __tablename__ = "sellers"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    representative_id = Column(Integer, ForeignKey('representatives.user_id'))
    seller_discount = Column(Numeric, default=0)
    user = relationship("User", back_populates="seller")
    representative = relationship("Representative", back_populates="sellers")

class EntryStatusEnum(enum.Enum):
    Restricao = "Restrição"
    Finalizado = "Finalizado"
    Reprotocolo = "Reprotocolo"

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)  # limpeza|rating
    doc = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    vendedor = Column(String)
    valor = Column(Numeric, nullable=False)
    desconto = Column(Numeric, nullable=False)
    liquido = Column(Numeric, nullable=False)
    status = Column(Enum(EntryStatusEnum), default=EntryStatusEnum.Restricao)
    feito = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    mime = Column(String)
    entry_id = Column(Integer, ForeignKey('entries.id'), nullable=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)