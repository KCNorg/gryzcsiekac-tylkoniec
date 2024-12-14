"""Update Order

Revision ID: 1e9092d60f28
Revises: 76dfa01cdc29
Create Date: 2024-12-14 17:02:51.315362

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1e9092d60f28"
down_revision: Union[str, None] = "76dfa01cdc29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ordercategory_enum = ENUM(
    "GROCERIES",
    "PET_WALKING",
    "CONVERSATION",
    "OTHER",
    name="ordercategory",
    native_enum=True,
)


def upgrade() -> None:
    # Create the new enum type
    ordercategory_enum.create(op.get_bind(), checkfirst=True)

    # # Alter the column to use the new enum type
    op.alter_column(
        "orders",
        "category",
        existing_type=sa.dialects.postgresql.ENUM(
            "SENIOR", "VOLUNTEER", name="usertype"
        ),
        type_=ordercategory_enum,
        existing_nullable=False,
        postgresql_using="category::text::ordercategory",
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "orders",
        "category",
        existing_type=postgresql.ENUM("SENIOR", "VOLUNTEER", name="usertype"),
        type_=sa.Enum(
            "GROCERIES", "PET_WALKING", "CONVERSATION", "OTHER", name="ordercategory"
        ),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # Revert the column to the old enum type
    op.alter_column(
        "orders",
        "category",
        existing_type=ordercategory_enum,
        type_=sa.dialects.postgresql.ENUM("SENIOR", "VOLUNTEER", name="usertype"),
        existing_nullable=False,
        postgresql_using="category::text::usertype",  # Explicitly cast the column values
    )

    # Drop the new enum type
    ordercategory_enum.drop(op.get_bind(), checkfirst=True)

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "orders",
        "category",
        existing_type=ordercategory_enum,
        type_=postgresql.ENUM("SENIOR", "VOLUNTEER", name="usertype"),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
