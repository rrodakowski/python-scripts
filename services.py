import time
from sys import argv
from subprocess import call
import logging

logger = logging.getLogger(__name__)

class FileService:
    'Contains helpful functions related to working with files'

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s %(message)s')

    def write_to_file(self,filename, text):
        logger.info("Writing the file: "+filename)
        file = open(filename, "w")
        for line in text:
            file.write(line+"\n")
        file.write("\n")
        file.close()

    def write_raw_text_to_file(self,filename, text):
        logger.info("Writing the file: "+filename)
        file = open(filename, "w")
        for line in text:
            file.write(line)
        file.close()

    def read_a_file(self, filename):
        logger.info("Reading the file: "+filename)
        file = open(filename, 'r')
        for line in file:
            logger.debug(line)

    def create_email_file(self, msg_subject, msg_body):
        logger.info("Creating an email file ")
        logtime=time.strftime("%Y%m%d")
        filename='/app-data/link_reporting_{}.log'.format(logtime)
        text=[]
        text.append(msg_subject)
        for line in msg_body:
            text.append(line)
        self.write_to_file(filename,text) 
        return filename

    def send_message(self, msg_subject, msg_body, server_info, email_address):
        logger.info("Send email message to: "+email_address)
        subject = 'subject: {} {} {}'.format(time.asctime(), msg_subject.upper(), server_info)
        email=self.create_email_file(subject, msg_body)
        call('sendmail -v {} < {}'.format(email_address, email), shell=True)
