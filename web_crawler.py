from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import traceback
import re
import argparse
 
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
                    newUrl = parse.urljoin(self.baseUrl, value)
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
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a website for phone numbers')
    parser.add_argument('-u', required=True, dest='starturl', action='store', help='the starting url')
    parser.add_argument('-m', type=int, dest='maxpages', action='store', help='maximum pages to crawl')
    args = parser.parse_args()

    pagesToVisit=[args.starturl]
    maxPages=args.maxpages
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
    
    
