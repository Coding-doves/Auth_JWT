from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from decouple import config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


config_mail = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(BASE_DIR, 'mail_template')
)

f_mail = FastMail(config=config_mail)


# Mail Validation
def mail_send(send_to: List[str], subject:str, body:str) -> str:

    message = MessageSchema(
        subject=subject,
        recipients=send_to,
        body=body,
        subtype=MessageType.html)

    return message
