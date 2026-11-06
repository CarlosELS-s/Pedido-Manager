import hashlib
import secrets
import random
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from models import Usuario
from dependecies import pegar_sessao, verificar_token
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSenhaSchema, EsqueciSenhaSchema, RedefinirSenhaSchema, FuncaoUsuarioSchema, EmailSchema, CodigoEmailSchema
from gmail_service import enviar_email

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _criar_tokens(usuario):
    from main import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

    agora = datetime.now(timezone.utc)
    base = {"sub": str(usuario.id), "admin": bool(usuario.admin), "funcao": usuario.funcao or "cliente"}
    access = jwt.encode({**base, "exp": agora + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
    refresh = jwt.encode({**base, "exp": agora + timedelta(days=7)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


def _criar_token_visitante():
    from main import SECRET_KEY, ALGORITHM

    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY não configurada no servidor.")

    payload = {
        "sub": "visitante",
        "nome": "Visitante",
        "visitante": True,
        "admin": False,
        "funcao": "visitante",
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    return {
        "access_token": jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer",
        "nome": "Visitante",
        "visitante": True
    }


@auth_router.get("/")
async def home():
    return {"message": "autenticando usuario", "status": True}


@auth_router.post("/visitante")
async def login_visitante():
    return _criar_token_visitante()


@auth_router.post("/criar_conta")
async def criar_conta(dados: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    email = dados.email.strip().lower() if dados.email else ""

    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Informe um e-mail válido.")
    if not dados.senha or len(dados.senha) < 8:
        raise HTTPException(status_code=400, detail="A senha precisa ter pelo menos 8 caracteres.")
    if len(dados.senha.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="A senha deve ter no máximo 72 bytes.")
    if session.query(Usuario).filter(Usuario.email.ilike(email)).first():
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    usuario = Usuario(
        nome=dados.nome.strip(),
        email=email,
        telefone=None,
        senha=bcrypt_context.hash(dados.senha),
        ativo=True,
        admin=False,
        funcao="cliente"
    )

    usuario.email_verificado = True
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return {"message": "Conta criada com sucesso.", "id": usuario.id, "nome": usuario.nome, "email": usuario.email}


@auth_router.post("/login")
async def login(dados: LoginSenhaSchema, session: Session = Depends(pegar_sessao)):
    email = dados.email.strip().lower()
    usuario = session.query(Usuario).filter(Usuario.email.ilike(email)).first()

    if not usuario or not usuario.senha or not bcrypt_context.verify(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="Esta conta está desativada.")

    return _criar_tokens(usuario)


@auth_router.post("/esqueci-senha")
async def esqueci_senha(dados: EsqueciSenhaSchema, session: Session = Depends(pegar_sessao)):
    email = dados.email.strip().lower()
    usuario = session.query(Usuario).filter(Usuario.email.ilike(email)).first()

    if usuario and usuario.ativo:
        token = secrets.token_urlsafe(32)
        usuario.token_redefinicao_senha = _hash_token(token)
        usuario.token_redefinicao_expira = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=30)
        frontend = __import__("os").getenv("FRONTEND_URL", "https://pedido-manager-three.vercel.app").rstrip("/")
        link = f"{frontend}/redefinir-senha?token={token}"

        html = f'<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto"><h2>Redefinição de senha</h2><p>Recebemos uma solicitação para redefinir a senha da sua conta PedidoManager.</p><p><a href="{link}" style="display:inline-block;padding:12px 18px;background:#0f172a;color:white;text-decoration:none;border-radius:8px">Criar nova senha</a></p><p>Este link expira em 30 minutos e só pode ser usado uma vez.</p><p>Se você não solicitou, ignore este e-mail.</p></div>'

        try:
            enviar_email(usuario.email, "Redefinição de senha - PedidoManager", html)
            session.commit()
        except Exception as erro:
            session.rollback()
            raise HTTPException(status_code=503, detail="Não foi possível enviar o e-mail agora. Verifique a configuração Gmail API no servidor.") from erro

    return {"message": "Se o e-mail estiver cadastrado, enviaremos um link de redefinição."}


@auth_router.post("/redefinir-senha")
async def redefinir_senha(dados: RedefinirSenhaSchema, session: Session = Depends(pegar_sessao)):
    if len(dados.senha) < 8:
        raise HTTPException(status_code=400, detail="A senha precisa ter pelo menos 8 caracteres.")
    if len(dados.senha.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="A senha deve ter no máximo 72 bytes.")

    usuario = session.query(Usuario).filter(Usuario.token_redefinicao_senha == _hash_token(dados.token)).first()
    agora = datetime.now(timezone.utc).replace(tzinfo=None)

    if not usuario or not usuario.token_redefinicao_expira or usuario.token_redefinicao_expira < agora:
        raise HTTPException(status_code=400, detail="Link inválido ou expirado. Solicite uma nova redefinição.")

    usuario.senha = bcrypt_context.hash(dados.senha)
    usuario.token_redefinicao_senha = None
    usuario.token_redefinicao_expira = None
    session.commit()

    return {"message": "Senha redefinida com sucesso. Faça login com sua nova senha."}


@auth_router.post("/adicionar-email/{id_usuario}")
async def adicionar_email(id_usuario: int, dados: EmailSchema, session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if atual.id != id_usuario:
        raise HTTPException(status_code=403, detail="Você não pode alterar o e-mail de outro usuário.")

    email = dados.email.strip().lower()
    existente = session.query(Usuario).filter(Usuario.email.ilike(email), Usuario.id != id_usuario).first()

    if existente:
        raise HTTPException(status_code=400, detail="Este e-mail já está em uso.")

    codigo = str(random.SystemRandom().randint(100000, 999999))
    atual.email = email
    atual.email_verificado = False
    atual.codigo_verificacao_email = codigo
    atual.codigo_verificacao_expira = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=10)
    session.commit()

    html = f'<p>Seu código de verificação do PedidoManager é <strong>{codigo}</strong>.</p><p>Ele expira em 10 minutos.</p>'

    try:
        enviar_email(email, "Verificação de e-mail - PedidoManager", html)
    except Exception as erro:
        raise HTTPException(status_code=503, detail="Não foi possível enviar o código pelo Gmail API.") from erro

    return {"mensagem": "Código enviado para o novo e-mail."}


@auth_router.post("/verificar-email/{id_usuario}")
async def verificar_email(id_usuario: int, dados: CodigoEmailSchema, session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if atual.id != id_usuario:
        raise HTTPException(status_code=403, detail="Você não pode verificar o e-mail de outro usuário.")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario or not usuario.codigo_verificacao_email or not usuario.codigo_verificacao_expira:
        raise HTTPException(status_code=400, detail="Nenhum código de verificação ativo.")

    agora = datetime.now(timezone.utc).replace(tzinfo=None)

    if usuario.codigo_verificacao_expira < agora:
        raise HTTPException(status_code=400, detail="O código expirou. Solicite outro.")
    if str(dados.codigo).strip() != usuario.codigo_verificacao_email:
        raise HTTPException(status_code=400, detail="Código incorreto.")

    usuario.email_verificado = True
    usuario.codigo_verificacao_email = None
    usuario.codigo_verificacao_expira = None
    session.commit()

    return {"mensagem": "E-mail verificado com sucesso.", "email_verificado": True}


@auth_router.get("/refresh")
async def refresh(usuario: Usuario = Depends(verificar_token)):
    return _criar_tokens(usuario)


@auth_router.get("/usuarios")
async def listar_usuarios(session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if not atual.admin:
        raise HTTPException(status_code=403, detail="Acesso permitido somente para administradores.")

    usuarios = session.query(Usuario).all()

    return [
        {
            "id": u.id,
            "nome": u.nome,
            "telefone": u.telefone,
            "email": u.email,
            "ativo": u.ativo,
            "admin": u.admin,
            "funcao": u.funcao,
            "email_verificado": u.email_verificado,
            "telefone_verificado": u.telefone_verificado
        }
        for u in usuarios
    ]


@auth_router.get("/usuarios/{usuario_id}")
async def informacao_usuario_admin(usuario_id: int, session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if not atual.admin:
        raise HTTPException(status_code=403, detail="Acesso permitido somente para administradores.")

    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return {
        "id": u.id,
        "nome": u.nome,
        "telefone": u.telefone,
        "email": u.email,
        "ativo": u.ativo,
        "admin": u.admin,
        "funcao": u.funcao,
        "email_verificado": u.email_verificado,
        "telefone_verificado": u.telefone_verificado
    }


@auth_router.patch("/usuarios/{usuario_id}/status")
async def alterar_status_usuario(usuario_id: int, session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if not atual.admin:
        raise HTTPException(status_code=403, detail="Acesso permitido somente para administradores.")

    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.id == atual.id:
        raise HTTPException(status_code=400, detail="Você não pode desativar sua própria conta.")
    if u.admin:
        raise HTTPException(status_code=400, detail="Contas de administrador não podem ser desativadas.")

    u.ativo = not u.ativo
    session.commit()
    session.refresh(u)

    return {"id": u.id, "nome": u.nome, "ativo": u.ativo, "admin": u.admin, "funcao": u.funcao, "email": u.email}


@auth_router.delete("/usuarios/{usuario_id}")
async def deletar_usuario(usuario_id: int, session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if not atual.admin:
        raise HTTPException(status_code=403, detail="Acesso permitido somente para administradores.")

    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.id == atual.id:
        raise HTTPException(status_code=400, detail="Você não pode excluir sua própria conta.")

    session.delete(u)
    session.commit()

    return {"message": f"Usuário {u.nome} deletado com sucesso"}


@auth_router.put("/usuarios/{usuario_id}/funcao")
async def alterar_funcao_usuario(usuario_id: int, dados: FuncaoUsuarioSchema, session: Session = Depends(pegar_sessao), atual: Usuario = Depends(verificar_token)):
    if not atual.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem alterar usuários.")

    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.id == atual.id and not dados.admin:
        raise HTTPException(status_code=400, detail="Você não pode remover seu próprio acesso de administrador.")
    if dados.funcao not in ["cliente", "atendente", "cozinheiro", "entregador", "dono"]:
        raise HTTPException(status_code=400, detail="Função inválida.")
    if u.admin and dados.funcao != u.funcao:
        raise HTTPException(status_code=400, detail="A função de um administrador não pode ser alterada.")

    u.funcao = dados.funcao
    u.admin = dados.admin
    session.commit()
    session.refresh(u)

    return {"id": u.id, "nome": u.nome, "email": u.email, "funcao": u.funcao, "admin": u.admin}