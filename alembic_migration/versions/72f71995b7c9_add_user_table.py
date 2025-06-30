"""add user table

Revision ID: 72f71995b7c9
Revises: d454a3f008b3
Create Date: 2025-06-29 14:16:07.075169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '72f71995b7c9'
down_revision: Union[str, Sequence[str], None] = 'd454a3f008b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
