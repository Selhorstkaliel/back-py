import os
import jwt
from fastapi import Depends, HTTPException, status, Request, Response
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from cryptography.hazmat.primitives import serialization
from .config import settings

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16)

def get_jwt_keys():
    # Gera e salva chaves se não existirem, ou carrega do .env
    priv = settings.JWT_PRIVATE_KEY
    pub = settings.JWT_PUBLIC_KEY
    if not priv or not pub:
        # Geração automática Ed25519
        from cryptography.hazmat.primitives.asymmetric import ed25519
        private_key = ed25519.Ed25519PrivateKey.generate()
        priv_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with open(".env", "a") as f:
            f.write(f'JWT_PRIVATE_KEY="{priv_bytes.decode()}"\n')
            f.write(f'JWT_PUBLIC_KEY="{pub_bytes.decode()}"\n')
        return priv_bytes, pub_bytes
    return priv.encode(), pub.encode()

def create_jwt(data: dict, expires_delta=timedelta(hours=8)):
    private_key, _ = get_jwt_keys()
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, private_key, algorithm="EdDSA")
    return token

def verify_jwt(token: str):
    _, public_key = get_jwt_keys()
    try:
        payload = jwt.decode(token, public_key, algorithms=["EdDSA"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return ph.verify(password_hash, password)
    except Exception:
        return False

def get_current_user(request: Request):
    token = request.cookies.get("jwt")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_jwt(token)
    return payload