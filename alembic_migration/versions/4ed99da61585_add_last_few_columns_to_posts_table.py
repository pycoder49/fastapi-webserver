"""add last few columns to posts table

Revision ID: 4ed99da61585
Revises: 7337391e5ffe
Create Date: 2025-06-29 19:06:30.742758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ed99da61585'
down_revision: Union[str, Sequence[str], None] = '7337391e5ffe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE")
    )

    op.add_column(
        "posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()"))
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
