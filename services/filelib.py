import csv
import os
import time
import logging
from subprocess import call
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)


class FileService(object):
    """Contains helpful functions related to working with files"""

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s %(message)s')

    @staticmethod
    def ensure_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def get_basename(path):
        return os.path.basename(path)

    @staticmethod
    def get_first_and_last_column(filename, separator):
        with file(filename, 'rb') as file_obj:
            for line in csv.reader(file_obj,
                delimiter=separator,    # Your custom delimiter.
                skipinitialspace=True): # Strips whitespace after delimiter.
                if line: # Make sure there's at least one entry.
                    yield line[0], line[-1]

    # useful for building novus load files
    @staticmethod
    def jar_files_in_dir(directory):
        for f in os.listdir(directory):
            if f.endswith(".gz"):
                no_ext=f[:-3]
                new_filename=no_ext+".jar"
                call('jar cvfM {} {}'.format(new_filename, f), shell=True)

    @staticmethod
    def write_to_file(filename, text):
        logger.info("Writing the file: "+filename)
        file = open(filename, "w")
        for line in text:
            file.write(line+"\n")
        file.write("\n")
        file.close()

    @staticmethod
    def write_raw_text_to_file(filename, text):
        logger.info("Writing the file: "+filename)
        file = open(filename, "w")
        for line in text:
            file.write(line)
        file.close()

    @staticmethod
    def read_a_file(filename):
        logger.info("Reading the file: "+filename)
        file = open(filename, 'r')
        for line in file:
            logger.debug(line)


class EmailService(object):
    """Contains helpful functions related to working with emails"""

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s %(message)s')
        self.fs = FileService()
        logger.info("Init for EmailService")

    def create_text_email(self, filename, msg_subject, msg_body):
        logger.info("Creating a plain text email file. ")
        # subject format: time subject from_server_info
        subject = 'subject: {} {} {}'.format(time.asctime(), msg_subject.upper(), "orangeshovel")
        text = []
        text.append(subject)
        for line in msg_body:
            text.append(line)
        self.fs.write_to_file(filename, text)

    def build_html_email(self, from_email, to_email, subject, text, html, output_email_file):
        logger.info("Creating an html email file. ")
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        self.fs.write_raw_text_to_file(output_email_file, msg.as_string())

    @staticmethod
    def send_email_file(email_file, to_email_address):
        logger.info("Send email message to: "+to_email_address)
        call('sendmail -v {} < {}'.format(to_email_address, email_file), shell=True)