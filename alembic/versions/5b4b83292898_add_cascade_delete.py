"""Add cascade delete

Revision ID: 5b4b83292898
Revises: 1e9092d60f28
Create Date: 2024-12-14 20:18:37.763516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b4b83292898'
down_revision: Union[str, None] = '1e9092d60f28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('orders_senior_id_fkey', 'orders', type_='foreignkey')
    op.drop_constraint('orders_volunteer_id_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'users', ['senior_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'orders', 'users', ['volunteer_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_volunteer_id_fkey', 'orders', 'users', ['volunteer_id'], ['id'])
    op.create_foreign_key('orders_senior_id_fkey', 'orders', 'users', ['senior_id'], ['id'])
    # ### end Alembic commands ###
