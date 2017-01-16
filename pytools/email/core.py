""" This module will provide smtp support for outgoing email and imap support for incoming mail. """

import email
import imaplib
import smtplib

from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from logging import getLogger


logger = getLogger(__name__)


class SMTPSender(object):

    def __init__(self, username, password, server, port):
        self._server = server
        self._port = port
        self._username = username
        self._password = password

        logger.debug("Created SMTP Sender.")

    def send(self, message: MIMEBase):
        logger.debug("Connecting to SMTP server")
        connection = smtplib.SMTP(self._server, self._port)
        logger.debug("Connected to SMTP server")

        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(self._username, self._password)
        logger.debug("Logged into SMTP server")

        connection.sendmail(message['From'], [message['To']], message.as_string())
        logger.debug("Mail sent")

        connection.quit()

    def __str__(self):
        return "{0}(username={1._username}, server={1._server}, port={1._port})".format(self.__class__.__name__, self)


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


class FailedToGetUnreadEmailError(RuntimeError):
    pass


class IMAPReceiver(object):

    def __init__(self, username, password, imap_server):

        self._username = username
        self._password = password
        self._server = imap_server

        logger.debug("Created IMAP Receiver.")

    @staticmethod
    def _build_query(from_addr, read):
        query = ""

        if from_addr:
            query = "(FROM \"{0}\"{1})".format(from_addr, " UNSEEN" if not read else "")
        elif read:
            query = "UNSEEN"

        return query

    def get_new_emails(self, from_addr=None, read=False) -> List[MIMEBase]:

        emails = []
        connection = None

        try:

            connection = imaplib.IMAP4_SSL(self._server)
            return_code, capabilities = connection.login(self._username, self._password)

            logger.debug("Logged into %s %s", self._server, connection.status('INBOX', '(MESSAGES UNSEEN)'))

            query = self._build_query(from_addr, read)

            #connection.select()
            connection.select(readonly=1)

            logger.debug("Searching mailbox: %s", query)

            return_code, raw_messages = connection.search(None, query)

            if return_code != "OK":
                raise FailedToGetUnreadEmailError("Get unread from IMAP server failed.")

            logger.debug("Raw messages: %s", raw_messages)

            message_numbers = raw_messages[0].split(b' ') if raw_messages != [b''] else []

            for num in message_numbers:
                logger.debug("Fetching email %s", num)

                typ, data = connection.fetch(num, '(RFC822)')

                msg = email.message_from_bytes(data[0][1])
                emails.append(msg)

        finally:
            if connection:
                connection.close()
                connection.logout()

        return emails

