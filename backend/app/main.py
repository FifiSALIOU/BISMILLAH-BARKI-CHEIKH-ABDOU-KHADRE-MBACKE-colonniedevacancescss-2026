from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import admin, auth, parents, users
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    origins = settings.cors_origins_list()
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(auth.router)
    app.include_router(parents.router)
    app.include_router(admin.router)
    app.include_router(users.router)

    @app.get("/")
    def root():
        return {
            "message": "API Colonie Vacances 2026 - OK",
            "health": "/health",
            "docs": "/docs",
        }

    @app.get("/health")
    def health():
        return {"ok": True}

    return app


app = create_app()

