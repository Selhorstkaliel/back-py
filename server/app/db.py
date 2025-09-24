from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import settings

DATABASE_URL = f"sqlite:///{settings.SQLITE_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))