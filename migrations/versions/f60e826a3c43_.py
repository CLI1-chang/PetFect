"""empty message

Revision ID: f60e826a3c43
Revises: e178ae731642
Create Date: 2021-11-15 17:22:06.660512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f60e826a3c43'
down_revision = 'e178ae731642'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animals', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'animals', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'animals', type_='foreignkey')
    op.drop_column('animals', 'owner_id')
    # ### end Alembic commands ###