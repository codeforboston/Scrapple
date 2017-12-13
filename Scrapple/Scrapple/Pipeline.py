import scrapy

class ItemCallback:
    def new_item(self, item):
	    self.callback(item)
	    print("Item gather got item")

    def set_callback(self, callback):
	    self.callback = callback

newItemCallback = ItemCallback()

class Pipeline(object):
    def process_item(self, item, spider):
        newItemCallback.new_item(item)