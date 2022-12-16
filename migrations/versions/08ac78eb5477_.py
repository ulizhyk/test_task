"""empty message

Revision ID: 08ac78eb5477
Revises: 49952fde9c90
Create Date: 2022-12-16 15:05:52.780618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '08ac78eb5477'
down_revision = '49952fde9c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_code_versions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('from_date', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('status', postgresql.ENUM('added', 'remove'), nullable=True),
    sa.Column('service_code_id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['service_code_id'], ['service_codes.id'], ),
    sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_code_versions')
    # ### end Alembic commands ###