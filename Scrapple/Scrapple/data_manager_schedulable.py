# data_manager_schedulable.py
import scrapy
from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from . import pipeline
from . import craig_spyder
from Database import dataFactory

#import multiprocessing
import schedule
import time


class DataManager:
    def __init__(self):
        self.__spiderMap = { "craigslist": 
                             {"spyder": craig_spyder.MySpider,
                             "schedule_title": "schedule.every(10).minutes.do(dummy_scrapy_job)",
                             "schedule_obj": schedule.every(10).minutes.do(dummy_scrapy_job),
                             "sch_proc": None,
                             "sch_que": None}
                            }
        # { "craigslist": craig_spyder.MySpider}
        pipeline.newItemCallback.set_callback(self.new_item_recieved)
        print("Data Manager started")
        self.__activeSpiders = {}
        
    @staticmethod
    def run_spider_in_thread(queue, spider):
        try:
            #runner = spider.CrawlerRunner()
            runner = CrawlerRunner(get_project_settings())
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as e:
            queue.put(e)


    def start_spider(self, strSpiderName):
        print("DataManager.start_spider")
        q = Queue()
        spider = self.__spiderMap[strSpiderName];
        thread = Process(target=self.run_spider_in_thread, args=(q,spider))
        thread.start()
        result = q.get()
        thread.join()
        
        if result is not None:
            print(result)

    
    # def run_spiders(self):
    #     # for spider, process in self.__activeSpiders.items():
    #     #     runner.start()
    #     #     process.stop()
    #     d = self.__runner.join()
    #     d.addBoth(lambda _: reactor.stop())
    #     reactor.run() # the script will block here until all crawling jobs are finished
    #     del self.__runner



    def start_spider_sch(self, strSpiderName):
        # in start_schedule methed
        print("Added spider schedule for" + strSpiderName)
        # set sch_que this in __spiderMap
        self.__spiderMap[strSpiderName]["sch_que"] = multiprocessing.Queue()
        self.__activeSpiders[strSpiderName] = "STARTED"
        # get scheduled_job this from __spiderMap
        scheduled_job = self.__spiderMap[strSpiderName]["schedule_obj"] #schedule.every(2).seconds.do(dummy_scrapy_job)
        # set sch_proc in __spiderMap
        self.__spiderMap[strSpiderName]["sch_proc"] = multiprocessing.Process(target=schedule_worker, args=(sch_que, scheduled_job))
        self.__spiderMap[strSpiderName]["sch_proc"].start()
        self.__spiderMap[strSpiderName]["sch_que"].put("START Scrapy schedule")
        time.sleep(6)


    def stop_spider_sch(self, strSpiderName):
        print("stop_spider depricated")
        if strSpiderName in self.__activeSpiders:
            self.__spiderMap[strSpiderName]["sch_que"].put("STOP")
            self.__spiderMap[strSpiderName]["sch_que"].close()
            self.__spiderMap[strSpiderName]["sch_que"].join_thread()
            self.__spiderMap[strSpiderName]["sch_proc"].join()
            # kill sch_proc Process
            del(self.__spiderMap[strSpiderName]["sch_proc"])
            del self.__activeSpiders[strSpiderName]

    def new_item_recieved(self, item):        
        dataFactory.listings_setter( item )

    def dummy_scrapy_job(self):
        print("I'm working at Scrapying...")

    def schedule_worker(self, sch_q, scheduled_job):
        scheduled_job
        q_mesg = sch_q.get()
        print ("q_mesg:",q_mesg)
        while q_mesg != "STOP":
            schedule.run_pending()
            if not sch_q.empty():
                q_mesg = sch_q.get()
                print ("q_mesg:",q_mesg)        
            time.sleep(1)

dataManager = DataManager()
