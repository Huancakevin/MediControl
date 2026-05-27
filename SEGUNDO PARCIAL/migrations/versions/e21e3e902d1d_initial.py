"""initial

Revision ID: e21e3e902d1d
Revises: 
Create Date: 2026-05-26 19:10:58.213177

"""
from alembic import op
import sqlalchemy as sa

revision = 'e21e3e902d1d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('medicos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=128), nullable=False),
    sa.Column('especialidad', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pacientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=128), nullable=False),
    sa.Column('telefono', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('citas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.Column('hora', sa.Time(), nullable=False),
    sa.Column('medico_id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['medico_id'], ['medicos.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('citas')
    op.drop_table('pacientes')
    op.drop_table('medicos')
