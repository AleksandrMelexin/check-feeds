import urllib.request as urllib2
from bs4 import BeautifulSoup as Soup

class FeedProcessing():
    def __init__(self, url):
        self.feedUrl = url
    
    def process(self):
        try:
            page = urllib2.urlopen(self.feedUrl).read()
            soup = Soup(page)
            names = [offer.find("name").text for offer in soup.find_all("offer")]
            print(names, sep="\n")
            return names
        except Exception as e:
            return str(e)
