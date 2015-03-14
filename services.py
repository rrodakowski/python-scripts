import urlparse, string, csv, os, time, logging
from sys import argv
from subprocess import call
from urllib2 import urlopen
from socket import socket



logger = logging.getLogger(__name__)

class FileService:
    'Contains helpful functions related to working with files'

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s %(message)s')

    def get_first_and_last_column(filename, separator):
        with file(filename, 'rb') as file_obj:
            for line in csv.reader(file_obj,
                delimiter=separator,    # Your custom delimiter.
                skipinitialspace=True): # Strips whitespace after delimiter.
                if line: # Make sure there's at least one entry.
                    yield line[0], line[-1]

    #useful for building novus load files
    def jar_files_in_dir(self, directory):
        for f in os.listdir(directory):
            if f.endswith(".gz"):
                no_ext=f[:-3]
                new_filename=no_ext+".jar"
                call('jar cvfM {} {}'.format(new_filename, f), shell=True)

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


class ServiceMonitor(object):

    def usage(self):
        print('%s <test-type> <server-info> <email-address>\n' % (argv[0]))
        print('\ttest-type    \ttcp or http')
        print('\tserver-info  \thostname:port for tcp')
        print('\t             \thttp://hostname/page for http')
        print('\temail-address\tusername or username@domain.com\n')

    def tcp_test(self, server_info):
        cpos = server_info.find(':')
        if cpos < 1 or cpos == len(server_info) - 1:
            print('You need to give server info as hostname:port.')
        self.usage()
        return True
        try:
            sock = socket()
            sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
            sock.close
            return True
        except:
            return False

    def http_test(self, server_info):
        try:
            data = urlopen(server_info).read()
            return True
        except:
            print('Could not read from the server')
            return False

    def server_test(self, test_type, server_info):
        if test_type.lower() == 'tcp':
            return self.tcp_test(server_info)
        elif test_type.lower() == 'http':
            return self.http_test(server_info)
        else:
            print('Invalid test-type given, please use either tcp or http.')
            return True

    def send_error(self, test_type, server_info, email_address):
        subject = '%s: %s %s error' % (time.asctime(), test_type.upper(), server_info)
        message = 'There was an error while executing a %s test against %s.' % (test_type.upper(), server_info)
        os.system('echo "%s" | mail -s "%s" %s' % (message, subject, email_address))

class ScreenScraper(object):

    def get_temperature(self, country, state, city):
        url = urlparse.urljoin('http://www.weather.com/weather/cities/',
                           string.lower(country)+'_' + \
                           string.lower(state) + '_' + \
                           string.replace(string.lower(city), ' ',
                                          '_') + '.html')
        data = urlopen(url).read()
        start = string.index(data, 'current temp: ') + len('current temp: ')
        stop = string.index(data, '&degv;F', start-1)
        temp = int(data[start:stop])
        localtime = time.asctime(time.localtime(time.time()))
        print('On {}, the temperature in {}, {}, {} is {}.'.format(localtime,city, state, country, temp))