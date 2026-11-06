
import os
import base64
import logging

from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def enviar_email(destino: str, assunto: str, html: str):
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")
    remetente = os.getenv("GMAIL_USER")

    if not all([
        client_id,
        client_secret,
        refresh_token,
        remetente
    ]):
        raise RuntimeError(
            "Variáveis do Gmail API ausentes. "
            "Verifique GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, "
            "GMAIL_REFRESH_TOKEN e GMAIL_USER."
        )

    try:
        credenciais = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )

        # Autentica explicitamente no Google
        credenciais.refresh(Request())

        # Cria o serviço Gmail
        servico = build(
            "gmail",
            "v1",
            credentials=credenciais,
            cache_discovery=False
        )

        # Monta o e-mail
        mensagem = MIMEText(
            html,
            "html",
            "utf-8"
        )

        mensagem["to"] = destino
        mensagem["from"] = remetente
        mensagem["subject"] = assunto

        raw = base64.urlsafe_b64encode(
            mensagem.as_bytes()
        ).decode("utf-8")

        # Envia
        resultado = (
            servico.users()
            .messages()
            .send(
                userId="me",
                body={"raw": raw}
            )
            .execute()
        )

        logger.info(
            "E-mail enviado com sucesso. ID: %s",
            resultado.get("id")
        )

        return resultado

    except Exception:
        logger.exception(
            "ERRO DETALHADO AO ENVIAR E-MAIL PELO GMAIL API"
        )
        raise
