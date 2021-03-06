"""parent_id in comment

Revision ID: 196174fb1992
Revises: 4388aea18d96
Create Date: 2021-08-24 11:50:44.792002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '196174fb1992'
down_revision = '4388aea18d96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_hierarchy')
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('parent_id')

    op.create_table('comment_hierarchy',
    sa.Column('parent_id', sa.INTEGER(), nullable=True),
    sa.Column('child_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['comment.id'], )
    )
    # ### end Alembic commands ###
