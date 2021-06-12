"""empty message

Revision ID: f55adb9a6e35
Revises: 97238dc91f8d
Create Date: 2021-06-12 13:17:17.912747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f55adb9a6e35'
down_revision = '97238dc91f8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rides', sa.Column('image', sa.String(length=200), nullable=True))
    op.add_column('rides', sa.Column('optional_notes', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rides', 'optional_notes')
    op.drop_column('rides', 'image')
    # ### end Alembic commands ###