# Backend Colonie de Vacances 2026 (CSS)

Backend API en **FastAPI + PostgreSQL**.

## Prérequis
- Python 3.11+
- PostgreSQL 14+

## Installation (Windows PowerShell)
Créer un environnement virtuel puis installer les dépendances :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration
Copier `.env.example` vers `.env` puis adapter la chaîne de connexion PostgreSQL.

## Migrations
```powershell
alembic upgrade head
```

## Lancer l’API
```powershell
uvicorn app.main:app --reload
```

## Initialiser le premier SUPER_ADMIN
Depuis `backend/` (après que la base PostgreSQL soit accessible) :
```powershell
python create_first_super_admin.py --email "superadmin@exemple.com" --password "MotDePasseSuperAdmin" --name "SUPER_ADMIN"
```

Documentation :
- Swagger: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

