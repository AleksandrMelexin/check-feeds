import urllib.request as urllib2
from bs4 import BeautifulSoup as Soup

class FeedProcessing():
    def __init__(self, url):
        self.feedUrl = url
    
    def process(self):
        try:
            page = urllib2.urlopen(self.feedUrl).read()
            soup = Soup(page, "xml")
            offers = []
            offersIds = []
            for offer in soup.find_all("offer"):
                offerItem = {}
                offerItem["errors"] = []
                offerName = offer.find("name")
                if offerName is None:
                    offerName = offer.find("model")
                    if offerName is None:
                        offerItem["errors"].append("Название товара не указано")
                        offerItem["name"] = ""
                    else:
                        offerItem["name"] = offerName.text
                else:
                    offerItem["name"] = offerName.text
                try:
                    offerItem["id"] = int(offer.attrs["id"])
                except:
                    offerItem["errors"].append("Отсутвует ID")
                    offerItem["id"] = "Пустой ID"

                if offerItem["id"] not in offersIds:
                    offersIds.append(offerItem["id"])
                elif offerItem["id"] != "Пустой ID":
                    offerItem["errors"].append("ID не является уникальным")
                pictures = offer.find_all("picture")
                offerItem["pictures"] = [picture.string for picture in pictures]
                if len(offerItem["pictures"]) < 1 or len(offerItem["pictures"]) > 5:
                    offerItem["errors"].append("Количество картинок не соответствует требованиям (от 1 до 5)")
                offers.append(offerItem)
            return offers
        except Exception as e:
            print(str(e))
            return str(e)
