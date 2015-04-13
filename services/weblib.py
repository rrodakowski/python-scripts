#! /usr/bin/env python

import traceback
import re
import argparse
import string
import time
import urlparse

# changed to Html.Parser in python3
from HTMLParser import HTMLParser

from os import system
from sys import argv
from time import asctime
from urllib2 import urlopen
from socket import socket


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
            sock.connect((server_info[:cpos], int(server_info[cpos + 1:])))
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
        subject = '%s: %s %s error' % (asctime(), test_type.upper(), server_info)
        message = 'There was an error while executing a %s test against %s.' % (test_type.upper(), server_info)
        system('echo "%s" | mail -s "%s" %s' % (message, subject, email_address))

    def main(self, test_type, server_info, email_address):
        if not self.server_test(argv[1], argv[2]):
            self.send_error(argv[1], argv[2], argv[3])


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


# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        #print("handle_start_tag {} with attrs {}.".format(tag, attrs))
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL.
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = urlparse.urljoin(self.baseUrl, value)
                    # And add it to our collection of links:
                    self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        header = response.getheader('Content-Type')
        if header =='text/html' or header =='text/html; charset=UTF-8':
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")

            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

    def main(self, pagesToVisit, maxPages):
        numberVisited=0
        foundWord = False

        # Create a LinkParser, get Links returns all the links
        # on the web page and the data. A regular expression is
        # used to find any phone numbers. If we find phone numbers, stop.
        # If we don't, go to the next page.
        while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
            numberVisited = numberVisited +1
            # Start from the beginning of our collection of pages to visit:
            url = pagesToVisit[0]
            pagesToVisit = pagesToVisit[1:]

            try:
                print(numberVisited, "Visiting:", url)
                parser = LinkParser()
                data, links = parser.getLinks(url)
                # Add the pages that we visited to the end of our collection
                # of pages to visit:
                pagesToVisit = pagesToVisit + links

                match = re.findall('\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4}', data)

                if match:
                    foundWord = True
                    print(" **Here are some phone numbers found at ", url)
                    for phone_number in match:
                        print(phone_number)

            except:
                print(" **Failed!**")
                traceback.print_exc()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a website for phone numbers')
    parser.add_argument('-u', required=True, dest='starturl', action='store', help='the starting url')
    parser.add_argument('-m', type=int, dest='maxpages', action='store', help='maximum pages to crawl')
    args = parser.parse_args()

    pagesToVisit=[args.starturl]
    maxPages=args.maxpages

    lp = LinkParser()
    lp.main(pagesToVisit, maxPages)

# main for th service monitor, took it out for the moment
#if __name__ == '__main__':
#    sm = ServiceMonitor()
#    if len(argv) != 4:
#        print('Wrong number of arguments.')
#        sm.usage()

#   sm.main(argv[1], argv[2], argv[3])

