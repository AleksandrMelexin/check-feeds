import urllib.request as urllib2
from bs4 import BeautifulSoup as Soup
import app
import classes.models as models
import classes.errors as errors

class FeedProcessing():
    def __init__(self, url):
        self.feedUrl = url

    def createFeed(self):
        feed = models.Feeds(url=self.feedUrl)
        with app.app.app_context():
            app.db.session.add(feed)
            app.db.session.commit()
            app.db.session.refresh(feed)
        return feed.id
    
    def createCheckFeed(self, feedId, pictureErrors, nameErrors, idErrors):
        checkFeed = models.CheckFeeds(feed_id=feedId, picture_error_count=pictureErrors, name_error_count=nameErrors, id_error_count=idErrors)
        with app.app.app_context():
            app.db.session.add(checkFeed)
            app.db.session.commit()

    def process(self):
        try:
            if self.feedUrl[-3:len(self.feedUrl)] != 'yml':
                raise errors.notYMLError('По указанному URL файл YML не найден')
            feedId = self.createFeed()
            page = urllib2.urlopen(self.feedUrl).read()
            soup = Soup(page, "xml")
            offers = []
            offersIds = []
            idErrors = 0
            nameErrors = 0
            pictureErrors = 0
            for offer in soup.find_all("offer"):
                offerItem = {}
                offerItem["errors"] = []
                offerName = offer.find("name")
                if offerName is None:
                    offerName = offer.find("model")
                    if offerName is None:
                        offerItem["errors"].append("Название товара не указано")
                        nameErrors += 1
                        offerItem["name"] = ""
                    else:
                        offerItem["name"] = offerName.text
                else:
                    offerItem["name"] = offerName.text
                try:
                    offerItem["id"] = int(offer.attrs["id"])
                except:
                    offerItem["errors"].append("Отсутвует ID")
                    idErrors += 1
                    offerItem["id"] = "Пустой ID"

                if offerItem["id"] not in offersIds:
                    offersIds.append(offerItem["id"])
                elif offerItem["id"] != "Пустой ID":
                    offerItem["errors"].append("ID не является уникальным")
                    idErrors += 1
                pictures = offer.find_all("picture")
                offerItem["pictures"] = [picture.string for picture in pictures]
                if len(offerItem["pictures"]) < 1 or len(offerItem["pictures"]) > 5:
                    offerItem["errors"].append("Количество картинок не соответствует требованиям (от 1 до 5)")
                    pictureErrors += 1
                offers.append(offerItem)
            self.createCheckFeed(feedId, pictureErrors, nameErrors, idErrors)
            if len(offers) == 0:
                raise errors.notYMLError('файл YML пуст')
            return offers
        except errors.notYMLError as warning:
            return {"globalWarning": str(warning)}
        except Exception as error:
            return {"globalError": str(error)}
