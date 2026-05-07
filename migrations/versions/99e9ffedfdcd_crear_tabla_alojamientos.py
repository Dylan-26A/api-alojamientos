"""crear tabla alojamientos

Revision ID: 99e9ffedfdcd
Revises: 3b78c2b8cf04
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa


revision = "99e9ffedfdcd"
down_revision = "3b78c2b8cf04"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "alojamientos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("precio_noche", sa.Numeric(10, 2), nullable=False),
        sa.Column("ciudad", sa.String(length=100), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("alojamientos")