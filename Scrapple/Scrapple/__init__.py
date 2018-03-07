from . import data_manager_schedulable 

class Scrapple:
    __scrapers = set()

    def intialize(self):
        print("The restartable scrapple has been initialized")

    def start_spider_sch(self, strScraperName):
        print("Starting " + strScraperName)
        data_manager_schedulable.dataManager.spider_sch(strScraperName)

    def stop_spider_sch(self, strScraperName):
        if strScraperName in self.__scrapers:
            print("Item is running. Stopping " + strScraperName)
            data_manager_schedulable.dataManager.stop_spider_sch(strScraperName)
        else :
            print(strScraperName + " is not current running")

    # def run_spiders(self):
    #     data_manager_schedulable.dataManager.run_spiders()


scrapple = Scrapple()