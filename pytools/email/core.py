""" This module will provide smtp support for outgoing email and imap support for incoming mail. """

import email
import imaplib
import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from logging import getLogger


logger = getLogger(__name__)


class SMTPSender(object):

    _smtp_server = ""
    _smtp_port = 0
    _username = ""
    _password = ""

    def __init__(self, username, password, smtp_server, smtp_port):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._username = username
        self._password = password

        logger.debug("Created SMTP Sender.")

    def send_email(self, mime_email):
        logger.info("Logging into SMTP server")
        smtp_connection = smtplib.SMTP(self._smtp_server, self._smtp_port)
        smtp_connection.ehlo()
        smtp_connection.starttls()
        smtp_connection.ehlo()
        smtp_connection.login(self._username, self._password)
        logger.debug("Logged into SMTP server")

        smtp_connection.sendmail(mime_email['From'], [mime_email['To']], mime_email.as_string())
        logger.debug("Mail sent")

        smtp_connection.quit()


def make_simple_text_message(from_address, to_address, subject, text):
    msg = MIMEText(text)

    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.preamble = 'text'

    return msg


def make_simple_image_message(from_address, to_address, subject, media):
    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.preamble = 'image'

    img = MIMEImage(media, 'jpg')

    msg.add_header('Content-Disposition', 'attachment', filename='image.jpg')
    msg.attach(img)

    return msg


class IMAPReceiver(object):
    _username = ""
    _password = ""
    _imap_server = ""

    def __init__(self, username, password, imap_server):

        self._username = username
        self._password = password
        self._imap_server = imap_server

        logger.debug("Created IMAP Receiver.")

    def get_new_emails(self):

        logger.debug("Logging into IMAP Server")

        emails = []

        imap_connection = imaplib.IMAP4_SSL(self._imap_server)
        return_code, capabilities = imap_connection.login(self._username, self._password)
        imap_connection.select(readonly=1)

        try:
            imap_connection.select()

            logger.debug("Logged into IMAP Server %s", imap_connection.status('INBOX', '(MESSAGES UNSEEN)'))

            return_code, raw_messages = imap_connection.search(None, 'UNSEEN')

            if return_code == "OK":
                for num in raw_messages[0].split(b' '):
                    logger.debug("Fetching email %s", num)

                    typ, data = imap_connection.fetch(num, '(RFC822)')

                    raw_email = data[0][1]

                    raw_email_string = raw_email.decode("utf-8")

                    msg = email.message_from_string(raw_email_string)
                    emails.append(msg)
        finally:
            imap_connection.close()
            imap_connection.logout()

        return emails

