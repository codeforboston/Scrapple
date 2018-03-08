from . import data_manager_schedulable 

class Scrapple:
    __scrapers = {}

    def intialize(self):
        print("The restartable scrapple has been initialized")

    def start_spider_sch(self, strScraperName):
        print("start_spider_sch> Starting " + strScraperName)
        data_manager_schedulable.dataManager.start_spider_sch(strScraperName)
        self.__scrapers[strScraperName] = True

    def stop_spider_sch(self, strScraperName):
        if strScraperName in self.__scrapers:
            print("Item is running. Stopping " + strScraperName)
            data_manager_schedulable.dataManager.stop_spider_sch(strScraperName)
            del(self.__scrapers[strScraperName])
        else :
            print("stop_spider_sch> ",strScraperName + " is not current running")

    # def run_spiders(self):
    #     data_manager_schedulable.dataManager.run_spiders()


scrapple = Scrapple()