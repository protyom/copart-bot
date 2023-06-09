"""initial

Revision ID: 0295fe83aac4
Revises: 
Create Date: 2023-03-26 10:30:07.016567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0295fe83aac4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_chat_chat_id'), 'chat', ['chat_id'], unique=True)
    op.create_index(op.f('ix_chat_id'), 'chat', ['id'], unique=False)
    op.create_table('lot',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lot_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('auction_date', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_lot_id'), 'lot', ['id'], unique=False)
    op.create_index(op.f('ix_lot_lot_id'), 'lot', ['lot_id'], unique=True)
    op.create_table('chat_lot_m2m',
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.UniqueConstraint('chat_id', 'lot_id', name='chat_lot_unique')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_lot_m2m')
    op.drop_index(op.f('ix_lot_lot_id'), table_name='lot')
    op.drop_index(op.f('ix_lot_id'), table_name='lot')
    op.drop_table('lot')
    op.drop_index(op.f('ix_chat_id'), table_name='chat')
    op.drop_index(op.f('ix_chat_chat_id'), table_name='chat')
    op.drop_table('chat')
    # ### end Alembic commands ###
