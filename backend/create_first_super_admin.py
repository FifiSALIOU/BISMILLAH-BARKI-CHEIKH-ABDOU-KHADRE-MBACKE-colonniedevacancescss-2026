from __future__ import annotations

import argparse

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.enums import UserRole
from app.models.models import User
from app.security import hash_password


def main() -> None:
    parser = argparse.ArgumentParser(description="Créer le premier SUPER_ADMIN (initialisation).")
    parser.add_argument("--email", required=True, help="Email du super admin")
    parser.add_argument("--password", required=True, help="Mot de passe du super admin (au moins 8 caractères)")
    parser.add_argument("--name", default="SUPER_ADMIN", help="Nom affiché")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existing = db.execute(select(User).where(User.role == UserRole.SUPER_ADMIN)).scalars().first()
        if existing:
            raise SystemExit("Un SUPER_ADMIN existe déjà dans la base. Arrêt.")

        user = User(
            role=UserRole.SUPER_ADMIN,
            email=args.email,
            matricule=None,
            password_hash=hash_password(args.password),
            name=args.name,
            is_active=True,
        )
        db.add(user)
        db.commit()
        print(f"SUPER_ADMIN créé: id={user.id}, email={user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

