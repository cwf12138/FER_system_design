"""empty message

Revision ID: 0bc974f9be4a
Revises: 
Create Date: 2023-05-04 16:37:50.472619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bc974f9be4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('aid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('number', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.Column('avater', sa.String(length=500), nullable=True),
    sa.Column('permission', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('aid', 'number')
    )
    op.create_table('user',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('number', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.Column('avater', sa.String(length=500), nullable=True),
    sa.Column('permission', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('uid', 'number')
    )
    op.create_table('camera',
    sa.Column('cid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('cameratime', sa.DateTime(), nullable=True),
    sa.Column('usagetime', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('cid')
    )
    op.create_table('picture',
    sa.Column('pid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('result', sa.String(length=50), nullable=True),
    sa.Column('picturetime', sa.DateTime(), nullable=True),
    sa.Column('picture_address', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pid')
    )
    op.create_table('video',
    sa.Column('vid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('videotime', sa.DateTime(), nullable=True),
    sa.Column('usagetime', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('picture')
    op.drop_table('camera')
    op.drop_table('user')
    op.drop_table('admin')
    # ### end Alembic commands ###
