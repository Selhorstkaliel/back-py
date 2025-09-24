import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .config import settings
from .routes import auth, users, entries, stats, charts, profile, support, contract

def get_app():
    app = FastAPI(title="LIMITCLEAN API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Adicione middlewares extras de segurança (helmet-like) aqui

    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/admin", tags=["users"])
    app.include_router(entries.router, prefix="/api/entries", tags=["entries"])
    app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
    app.include_router(charts.router, prefix="/api/charts", tags=["charts"])
    app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
    app.include_router(support.router, prefix="/api/tickets", tags=["support"])
    app.include_router(contract.router, prefix="/api/contract", tags=["contract"])

    return app

app = get_app()