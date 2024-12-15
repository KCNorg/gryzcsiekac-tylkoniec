"""Merge heads

Revision ID: b39cb5c128d1
Revises: 71670c745310, c494ed642329
Create Date: 2024-12-15 01:54:46.523935

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b39cb5c128d1"
down_revision: Union[str, None] = ("71670c745310", "c494ed642329")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
