import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from . import Pipeline
from . import CraigSpyder

class DataManager:
    def __init__(self):
        self.spiderMap = { "craigslist": CraigSpyder.MySpider}
        Pipeline.newItemCallback.set_callback(self.new_item)
        print("Data Manager started")
        self.activeSpiders = {}
        

    def start_spider(self, strSpiderName):
        print("Added spider " + strSpiderName)
        process = CrawlerProcess(get_project_settings())
        process.crawl(self.spiderMap[strSpiderName])

        self.activeSpiders[strSpiderName] = process

    def run_spiders(self):
        for spider, process in self.activeSpiders.items():
            process.start()

    def new_item(self, item):
        print("New Item")

dataManager = DataManager()