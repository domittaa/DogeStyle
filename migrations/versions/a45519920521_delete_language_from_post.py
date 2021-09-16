"""delete language from post

Revision ID: a45519920521
Revises: 58e4b015e6c8
Create Date: 2021-09-01 09:59:53.499449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a45519920521'
down_revision = '58e4b015e6c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('language')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.VARCHAR(length=5), nullable=True))

    # ### end Alembic commands ###