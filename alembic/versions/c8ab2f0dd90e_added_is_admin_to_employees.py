"""Added is_admin to employees

Revision ID: c8ab2f0dd90e
Revises: 21d2fe7ca352
Create Date: 2024-05-22 23:51:41.972367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8ab2f0dd90e'
down_revision: Union[str, None] = '21d2fe7ca352'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('is_admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees', 'is_admin')
    # ### end Alembic commands ###
