"""answer column in comment

Revision ID: 8967797ebaf6
Revises: c9497dc41e00
Create Date: 2021-08-24 07:12:06.630690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8967797ebaf6'
down_revision = 'c9497dc41e00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('answer')

    # ### end Alembic commands ###
