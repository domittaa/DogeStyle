"""avatar delete

Revision ID: 58e4b015e6c8
Revises: e3a6b55a7551
Create Date: 2021-08-31 08:33:30.112212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58e4b015e6c8'
down_revision = 'e3a6b55a7551'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('avatar_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_url', sa.TEXT(), nullable=True))

    # ### end Alembic commands ###