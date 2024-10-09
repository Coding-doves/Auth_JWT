"""
from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.config.mail_setup import f_mail, mail_send
from app.models.mail_model import EmailModel 


router = APIRouter()



@router.post("/send")
async def send_mail(emails: EmailModel) -> JSONResponse:
    send_to = [emails.email_address]

    html = "<h1>Nice verification</h1>"

    message = mail_send(
        subject="Welcome",
        recipients=send_to,
        body=html
        )

    await f_mail.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     
"""

