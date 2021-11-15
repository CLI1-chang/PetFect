"""merging two heads

Revision ID: e178ae731642
Revises: 9fc8edd26a4a, bfc228e5397f
Create Date: 2021-11-15 12:08:38.861194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e178ae731642'
down_revision = ('9fc8edd26a4a', 'bfc228e5397f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
