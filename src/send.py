import logging

from smtplib import SMTP_SSL

from . import util

logging.basicConfig(level=logging.DEBUG)


def prepare_body(address: str) -> str:
    config: dict = util.read_config()
    gmail_config: dict = config.get("gmail", {})

    uid = util.create_record(address)
    backend_host = config.get("host") + "/" + uid
    email_from = gmail_config.get("from")

    return util.EMAIL_BODY % (email_from, address, backend_host)


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
