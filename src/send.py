import logging

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from . import util

logging.basicConfig(level=logging.DEBUG)


def prepare_body(address: str) -> str:
    config: dict = util.read_config()
    gmail_config: dict = config.get("gmail", {})

    record = util.create_record(address)
    args = tuple(f"{config.get('host')}/{uid}" for uid in record[:2])
    email_from = gmail_config.get("from")

    msg = MIMEMultipart("alternative")
    email_body = MIMEText((util.EMAIL_BODY % args).encode("utf-8"), "html", "utf-8")
    msg.set_charset("utf8")

    msg["From"] = email_from
    msg["To"] = address
    msg["Subject"] = Header(util.EMAIL_SUBJECT.encode("utf-8"), "utf-8").encode()
    msg.attach(email_body)

    return msg.as_string()


def send_email(address: str) -> None:
    config: dict = util.read_config()
    gmail_config: dict = config.get("gmail", {})

    try:
        server = SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_config.get("login"), gmail_config.get("password"))
        server.sendmail(gmail_config.get("from"), address, prepare_body(address))
        logging.info(f"Email to {address} was sent")
        server.close()
    except Exception as ex:
        logging.error(f"Failed to send email: {ex}")
