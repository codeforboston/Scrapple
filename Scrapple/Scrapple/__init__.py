from scrapy_beautifulsoup import *
import scrapy_crawlera

class Scrapple:
    __scrapers = set()

    def Intialize(self):
        
        print("The scrapple has been initialized")

    def RunScraper(self, strScraperName):
        print("Starting " + strScraperName)
        self.__scrapers.add(strScraperName)

    def StopScraper(self, strScraperName):
        if strScraperName in self.__scrapers:
            print("Item is running. Stopping " + strScraperName)
        else :
            print(strScraperName + " is not current running")


scrapple = Scrapple();