"""initial tables

Revision ID: 0001
Revises:
Create Date: 2026-09-21

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "warehouse",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_warehouse"),
        sa.UniqueConstraint("name", name="uq_warehouse_name"),
    )
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(length=40), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouse.id"], name="fk_item_warehouse_id_warehouse"),
        sa.PrimaryKeyConstraint("id", name="pk_item"),
        sa.UniqueConstraint("sku", name="uq_item_sku"),
    )


def downgrade() -> None:
    op.drop_table("item")
    op.drop_table("warehouse")
