"""adicionar redefinicao de senha e email sem telefone"""
from alembic import op
import sqlalchemy as sa

revision = "d1a2b3c4d5e6"
down_revision = "1380e285239f"
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column("usuarios", "telefone", existing_type=sa.String(), nullable=True)
    op.add_column("usuarios", sa.Column("token_redefinicao_senha", sa.String(), nullable=True))
    op.add_column("usuarios", sa.Column("token_redefinicao_expira", sa.DateTime(), nullable=True))
    op.create_unique_constraint("uq_usuarios_token_redefinicao_senha", "usuarios", ["token_redefinicao_senha"])

def downgrade():
    op.drop_constraint("uq_usuarios_token_redefinicao_senha", "usuarios", type_="unique")
    op.drop_column("usuarios", "token_redefinicao_expira")
    op.drop_column("usuarios", "token_redefinicao_senha")
    op.alter_column("usuarios", "telefone", existing_type=sa.String(), nullable=False)
