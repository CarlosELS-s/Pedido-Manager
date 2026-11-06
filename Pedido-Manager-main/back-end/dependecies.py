from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from models import db, Usuario
from main import SECRET_KEY, ALGORITHM

oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


def pegar_sessao():
    session = sessionmaker(bind=db)()
    try:
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth_schema), session: Session = Depends(pegar_sessao)):
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY não configurada no servidor.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=401, detail="Usuário não encontrado ou inativo.")

    return usuario


def verificar_visitante(token: str = Depends(oauth_schema)):
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY não configurada no servidor.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    if payload.get("sub") != "visitante" or payload.get("visitante") is not True or payload.get("admin") is not False:
        raise HTTPException(status_code=403, detail="Acesso permitido somente para visitantes.")

    return payload