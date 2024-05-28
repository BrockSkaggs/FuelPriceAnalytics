from dotenv import load_dotenv
#Reference: https://youtu.be/g_j6ILT-X0k
from email.message import EmailMessage
import os
import ssl
import smtplib

load_dotenv()

email_sender = os.environ.get('email_sender')
email_pwd = os.environ.get('email_pwd')

def send_mail(recip: str, subject: str, body: str):
    email = EmailMessage()
    email['From'] = email_sender
    email["To"] = recip
    email["Subject"] = subject
    email.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pwd)
        smtp.sendmail(email_sender, recip, email.as_string())

def test():
    body = 'This is a test email!'
    print('test complete!')

if __name__ == '__main__':
    test()