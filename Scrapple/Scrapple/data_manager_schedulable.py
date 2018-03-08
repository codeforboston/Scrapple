# data_manager_schedulable.py
#import scrapy
from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from . import pipeline
from . import craig_spyder
from Database import dataFactory
import schedule


class DataManager:
    def __init__(self):
        # [spyder_obj] is the name of the object that contains a Scrapy spider
        # [schedule_obj] contains a schedule schedule object see https://schedule.readthedocs.io/en/stable/
        self.__spiderMap = {"craigslist":
                            {"spyder_obj": craig_spyder.MySpider,
                             "schedule_title": "schedule.every(10).minutes.do(self.dummy_scrapy_job)",
                             "schedule_obj": schedule.every(120).seconds.do(self.start_spider, strSpiderName="craigslist"),
                             "sch_proc": None,
                             "sch_que": None}
                            }
        pipeline.newItemCallback.set_callback(self.new_item_recieved)
        print("Data Manager started")
        self.__activeSpiders = {}

    @staticmethod
    def run_spider_in_thread(queue, spider):
        # runs the troublesum CrawlerRunner which never properly stops
        # killing this process will properly terminate CrawlerRunner
        try:
            runner = CrawlerRunner(get_project_settings())
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    def start_spider(self, strSpiderName):
        # manages launching and cleaning up run_spider_in_thread in its own process
        print("start_spider> ",strSpiderName)
        q = Queue()
        spider = self.__spiderMap[strSpiderName]["spyder_obj"]
        thread = Process(target=self.run_spider_in_thread, args=(q, spider))
        thread.start()
        result = q.get()
        thread.join()
        if result is not None:
            print(result)
    
    def start_spider_sch(self, strSpiderName):
        if strSpiderName not in self.__activeSpiders:
            print("start_spider_sch> Added spider schedule for " + strSpiderName)
            self.__spiderMap[strSpiderName]["sch_que"] = Queue()
            self.__activeSpiders[strSpiderName] = "STARTED"
            scheduled_job = self.__spiderMap[strSpiderName]["schedule_obj"]  
            self.__spiderMap[strSpiderName]["sch_proc"] = \
                Process(target=self.schedule_worker,
                                        args=(self.__spiderMap[strSpiderName]["sch_que"], scheduled_job))
            self.__spiderMap[strSpiderName]["sch_proc"].start()
            self.__spiderMap[strSpiderName]["sch_que"].put("START Scrapy schedule")
            print("start_spider_sch> START Scrapy schedule for", strSpiderName)
        else:
            print(strSpiderName, "alrede scheduled, stop first") # is this nesasry?

    def stop_spider_sch(self, strSpiderName): 
        print("stop_spider_sch> activeSpiders ")       
        if strSpiderName in self.__activeSpiders:
            print("stop_spider_sch> stoping schedule for ",strSpiderName)
            # this tells schedule_worker to stop running
            self.__spiderMap[strSpiderName]["sch_que"].put("STOP")
            # the following joins up the threads of the terminating process 
            self.__spiderMap[strSpiderName]["sch_que"].close()
            self.__spiderMap[strSpiderName]["sch_que"].join_thread()
            self.__spiderMap[strSpiderName]["sch_proc"].join()
            # now kill the sch_proc Process
            del(self.__spiderMap[strSpiderName]["sch_proc"])
            del(self.__activeSpiders[strSpiderName])
            # everything should now be cleaned out 
            print(strSpiderName, " schedule removed")
        else:
            print("stop_spider_sch> No schedule active for ", strSpiderName)

    def new_item_recieved(self, item):
        dataFactory.listings_setter(item)

    # def dummy_scrapy_job(self):
    #     print("I'm working at Scrapying...")

    def schedule_worker(self, sch_q, scheduled_job):
        # sets of predefined schedule using scheduled_job obj
        scheduled_job
        q_mesg = sch_q.get()
        print ("schedule_worker> q_mesg:", q_mesg)
        while q_mesg != "STOP":
            schedule.run_pending()
            if not sch_q.empty():
                q_mesg = sch_q.get()
                print ("schedule_worker> q_mesg:", q_mesg)


dataManager = DataManager()
