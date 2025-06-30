"""add column to post table

Revision ID: d454a3f008b3
Revises: 84659b19a64c
Create Date: 2025-06-29 14:04:14.577462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd454a3f008b3'
down_revision: Union[str, Sequence[str], None] = '84659b19a64c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
