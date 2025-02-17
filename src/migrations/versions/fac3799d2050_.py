"""empty message

Revision ID: fac3799d2050
Revises: 
Create Date: 2024-08-08 19:03:31.918420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fac3799d2050'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacancies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('compensation', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resumes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('compensation', sa.Integer(), nullable=True),
    sa.Column('workload', sa.Enum('parttime', 'fulltime', name='workload'), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc',now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc',now())"), nullable=False),
    sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies_replies',
    sa.Column('resumes_id', sa.Integer(), nullable=False),
    sa.Column('vacancies_id', sa.Integer(), nullable=False),
    sa.Column('cover_latter', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['resumes_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancies_id'], ['vacancies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('resumes_id', 'vacancies_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancies_replies')
    op.drop_table('resumes')
    op.drop_table('workers')
    op.drop_table('vacancies')
    # ### end Alembic commands ###
