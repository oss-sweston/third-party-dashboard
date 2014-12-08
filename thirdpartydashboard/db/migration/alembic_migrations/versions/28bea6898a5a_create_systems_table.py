"""create_systems_table

Revision ID: 28bea6898a5a
Revises: 
Create Date: 2014-12-08 17:57:59.696618

"""

# revision identifiers, used by Alembic.
revision = '28bea6898a5a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(active_plugins=None, options=None):
    op.create_table(
        'systems',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=50), nullable=True),
                sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uniq_systems_name'),
        sa.ForeignKeyConstraint(['operator_id'], ),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine=MYSQL_ENGINE,
        mysql_charset=MYSQL_CHARSET
    )

    op.create_table(
        'system_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('event_type', sa.Unicode(length=100), nullable=False),
        sa.Column('event_info', sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_engine=MYSQL_ENGINE,
        mysql_charset=MYSQL_CHARSET)


def downgrade():
    pass
