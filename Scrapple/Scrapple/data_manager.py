import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from . import pipeline
from . import craig_spyder
from Database import dataFactory


class DataManager:
    def __init__(self):
        self.__spiderMap = { "craigslist": craig_spyder.MySpider}
        pipeline.newItemCallback.set_callback(self.new_item_recieved)
        print("Data Manager started")
        self.__activeSpiders = {}
        
    def start_spider(self, strSpiderName):
        print("Added spider " + strSpiderName)
        process = CrawlerProcess(get_project_settings())
        process.crawl(self.__spiderMap[strSpiderName])

        self.__activeSpiders[strSpiderName] = process

    def stop_spider(self, strSpiderName):
        if strSpiderName in self.__activeSpiders:
            del self.__activeSpiders[strSpiderName]

    def run_spiders(self):
        for spider, process in self.__activeSpiders.items():
            process.start()

    def new_item_recieved(self, item):        
        dataFactory.listings_setter( item )

dataManager = DataManager()