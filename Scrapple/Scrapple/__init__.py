from . import data_manager_schedulable 

class Scrapple:
    __scrapers = {}

    def intialize(self):
        print("The restartable scrapple has been initialized")

    def start_spider_sch(self, strScraperName):
        print("start_spider_sch> Starting " + strScraperName)
        response = data_manager_schedulable.dataManager.start_spider_sch(strScraperName)
        self.__scrapers[strScraperName] = True
        return response

    def stop_spider_sch(self, strScraperName):
        if strScraperName in self.__scrapers:
            print("Item is running. Stopping " + strScraperName)
            response = data_manager_schedulable.dataManager.stop_spider_sch(strScraperName)
            del(self.__scrapers[strScraperName])
        else :
            response = "stop_spider_sch> " + strScraperName + " is not current running"
        return response



scrapple = Scrapple()