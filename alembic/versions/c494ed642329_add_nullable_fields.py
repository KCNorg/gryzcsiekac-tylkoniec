"""Add cascade delete

Revision ID: c494ed642329
Revises: 5b4b83292898
Create Date: 2024-12-15 00:34:06.973410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c494ed642329'
down_revision: Union[str, None] = '5b4b83292898'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('orders', 'valid_since',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('orders', 'valid_until',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'valid_until',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('orders', 'valid_since',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('orders', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
