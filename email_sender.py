import os
import smtplib
from email.message import EmailMessage

def send_email():
    email = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    to_email = os.getenv("TO_EMAIL")
    message = os.getenv("MESSAGE")

    if not all([email, password, to_email, message]):
        raise ValueError("Missing environment variables")

    msg = EmailMessage()
    msg["From"] = email
    msg["To"] = to_email
    msg["Subject"] = "Tama bel fee"
    msg.set_content(message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)

    print("Email sent successfully")
