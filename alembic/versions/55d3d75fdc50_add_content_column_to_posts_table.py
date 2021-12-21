"""add content column to posts table

Revision ID: 55d3d75fdc50
Revises: c14893a27610
Create Date: 2021-12-21 20:27:17.000444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55d3d75fdc50'
down_revision = 'c14893a27610'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
