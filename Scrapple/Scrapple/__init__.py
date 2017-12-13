from . import data_manager 

class Scrapple:
    __scrapers = set()

    def intialize(self):
        print("The scrapple has been initialized")

    def start_scraper(self, strScraperName):
        print("Starting " + strScraperName)
        data_manager.dataManager.start_spider(strScraperName)

    def stop_scraper(self, strScraperName):
        if strScraperName in self.__scrapers:
            print("Item is running. Stopping " + strScraperName)
        else :
            print(strScraperName + " is not current running")

    def run_spiders(self):
        data_manager.dataManager.run_spiders()


scrapple = Scrapple()