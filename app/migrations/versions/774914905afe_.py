"""empty message

Revision ID: 774914905afe
Revises: 8209201adcd7
Create Date: 2020-03-30 17:27:13.429695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '774914905afe'
down_revision = '8209201adcd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_fighters',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fighter_name', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'fighter_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_fighters')
    # ### end Alembic commands ###