from . import DataManager 

class Scrapple:
    __scrapers = set()

    def intialize(self):
        print("The scrapple has been initialized")

    def start_scraper(self, strScraperName):
        print("Starting " + strScraperName)
        DataManager.dataManager.start_spider(strScraperName)

    def StopScraper(self, strScraperName):
        if strScraperName in self.__scrapers:
            print("Item is running. Stopping " + strScraperName)
        else :
            print(strScraperName + " is not current running")

    def run_spiders(self):
        DataManager.dataManager.run_spiders


scrapple = Scrapple()