"""initial_tables

Revision ID: 12f5a539f16f
Revises: 
Create Date: 2014-12-08 20:56:38.468330

"""

# revision identifiers, used by Alembic.
revision = '12f5a539f16f'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

MYSQL_ENGINE = 'InnoDB'
MYSQL_CHARSET = 'utf8'

def upgrade():
    op.create_table(
        'systems',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=50), nullable=True),
                sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uniq_systems_name'),
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
    os.drop_table('systems')
    op.drop_table('system_events')
