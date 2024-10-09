from fastapi import FastAPI
from app.routers import post, user #, mail
from app.config.database import Base, engine  # Import declarative Base

#Base.metadata.drop_all(engine)  # This delete the tables
Base.metadata.create_all(engine)  # This creates the tables

app = FastAPI()

app.include_router(post.router, prefix="/posts", tags=["Post"])
app.include_router(user.router, prefix="/user", tags=["User"])
#app.include_router(mail.router, prefix="/email", tags=["Mail"])

import smtplib
from decouple import config
from email.message import EmailMessage
server = smtplib.SMTP('smtp.gmail.com', 587)

try:
    # Set up the SMTP server
    server.starttls()

    # Log in to your Gmail account
    server.login(config("MAIL_FROM"), config("MAIL_PASSWORD"))

    # Get the recipient's email
    send_to = input("Enter recipient email: ")

    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = "Verification"
    msg['From'] = config("MAIL_FROM")
    msg['To'] = send_to
    msg.set_content("You are Verified!")

    # Send the email
    server.send_message(msg)
    print("Email sent successfully.")

except smtplib.SMTPConnectError as e:
    print(f"Failed to connect to the SMTP server: {e}")
except smtplib.SMTPAuthenticationError as e:
    print(f"Failed to authenticate with Gmail: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    server.quit()

