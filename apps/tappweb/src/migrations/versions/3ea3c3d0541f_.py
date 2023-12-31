"""empty message

Revision ID: 3ea3c3d0541f
Revises: 331aae735676
Create Date: 2023-08-14 19:09:24.457075

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ea3c3d0541f'
down_revision = '331aae735676'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin_created', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('system_password', sa.Boolean(), nullable=True))
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_index('ix_users_phone', table_name='users')
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.drop_column('users', 'login_attempts')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'last_login_attempt')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login_attempt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('login_attempts', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.create_index('ix_users_phone', 'users', ['phone'], unique=False)
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_column('users', 'system_password')
    op.drop_column('users', 'admin_created')
    # ### end Alembic commands ###
