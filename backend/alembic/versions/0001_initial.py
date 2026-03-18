"""Initial schema.

Revision ID: 0001_initial
Revises: 
Create Date: 2026-03-18
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("matricule", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("PARENT", "GESTIONNAIRE", "SUPER_ADMIN", name="user_role"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_users_matricule", "users", ["matricule"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nom", sa.String(length=255), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nom", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "parents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("prenom", sa.String(length=255), nullable=False),
        sa.Column("nom", sa.String(length=255), nullable=False),
        sa.Column("matricule", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("telephone", sa.String(length=50), nullable=True),
        sa.Column("genre", sa.String(length=30), nullable=True),
        sa.Column("nin", sa.String(length=50), nullable=True),
        sa.Column("adresse", sa.Text(), nullable=True),
        sa.Column("service_id", sa.Integer(), sa.ForeignKey("services.id"), nullable=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_parents_matricule", "parents", ["matricule"], unique=True)

    op.create_table(
        "enfants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("parents.id"), nullable=False),
        sa.Column("prenom", sa.String(length=255), nullable=False),
        sa.Column("nom", sa.String(length=255), nullable=False),
        sa.Column("date_naissance", sa.Date(), nullable=False),
        sa.Column("sexe", sa.Enum("M", "F", name="sexe"), nullable=False),
        sa.Column(
            "lien_parente",
            sa.Enum("PERE", "MERE", "TUTEUR_LEGAL", "AUTRE", name="lien_parente"),
            nullable=False,
        ),
        sa.Column("is_titulaire", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_enfants_parent_id", "enfants", ["parent_id"], unique=False)

    op.create_table(
        "listes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "code",
            sa.Enum("PRINCIPALE", "ATTENTE_N1", "ATTENTE_N2", name="liste_code"),
            nullable=False,
            unique=True,
        ),
        sa.Column("nom", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "demandes_inscription",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("enfant_id", sa.Integer(), sa.ForeignKey("enfants.id"), nullable=False),
        sa.Column("liste_id", sa.Integer(), sa.ForeignKey("listes.id"), nullable=False),
        sa.Column("date_inscription", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("rang_dans_liste", sa.Integer(), nullable=False),
        sa.Column("is_selection_finale", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("selected_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("selected_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("enfant_id", name="uq_demande_enfant"),
        sa.UniqueConstraint("liste_id", "rang_dans_liste", name="uq_liste_rang"),
    )
    op.create_index("ix_demandes_inscription_liste_id", "demandes_inscription", ["liste_id"], unique=False)

    op.create_table(
        "desistements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "demande_inscription_id",
            sa.Integer(),
            sa.ForeignKey("demandes_inscription.id"),
            nullable=False,
        ),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("validated", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("validated_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.UniqueConstraint("demande_inscription_id", name="uq_desistement_demande"),
    )


def downgrade() -> None:
    op.drop_table("desistements")
    op.drop_index("ix_demandes_inscription_liste_id", table_name="demandes_inscription")
    op.drop_table("demandes_inscription")
    op.drop_table("listes")
    op.drop_index("ix_enfants_parent_id", table_name="enfants")
    op.drop_table("enfants")
    op.drop_index("ix_parents_matricule", table_name="parents")
    op.drop_table("parents")
    op.drop_table("sites")
    op.drop_table("services")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_matricule", table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS liste_code")
    op.execute("DROP TYPE IF EXISTS lien_parente")
    op.execute("DROP TYPE IF EXISTS sexe")
    op.execute("DROP TYPE IF EXISTS user_role")

