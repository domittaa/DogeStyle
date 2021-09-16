"""comment hierarchy

Revision ID: 4388aea18d96
Revises: 8967797ebaf6
Create Date: 2021-08-24 07:47:28.556110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4388aea18d96'
down_revision = '8967797ebaf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment_hierarchy',
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('child_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['comment.id'], )
    )
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('answer')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer', sa.INTEGER(), nullable=True))

    op.drop_table('comment_hierarchy')
    # ### end Alembic commands ###
