"""empty message

Revision ID: 39bd94a130d9
Revises: 0b13e34d7eec
Create Date: 2025-03-02 21:40:32.163716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39bd94a130d9'
down_revision = '0b13e34d7eec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(length=65536), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('chapter',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(length=65536), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.JSON(), nullable=True),
    sa.Column('chapter_id', sa.Integer(), nullable=False),
    sa.Column('question_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapter.id'], ),
    sa.ForeignKeyConstraint(['question_type_id'], ['question_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    op.drop_table('chapter')
    op.drop_table('subject')
    op.drop_table('question_type')
    # ### end Alembic commands ###
