import time
import schedule


class TradeController(object):
    
    def __init__(self, time_config) -> None:
        self.__feeds_interval = time_config["feeds"]
        self.__ind_interval = time_config["indicator"]
        self.__train_interval = time_config["model"]

    def register(self, model):
        self.__model = model
        self.__strategy = model.elect()
        self.__center = self.__model.__center

    def getMarket(self, crypto):
        self.__market = self.__center.get_crypto_current(crypto)
    
    def recalIndicator(self):
        new_feeds = self.__center.appendFeeds(self.__market)
        start = self.__center.__start
        end = now #TODO
        self.__center.__refresh(new_feeds, start, end)

        self.__strategy.execute(self.__market)

    def retrainModel(self):
        #TODO
        pass

    def run(self):
        schedule.every(self.__feeds_interval).minutes.do(self.getFeeds)
        schedule.every(self.__ind_interval).minutes.do(self.recalIndicator)
        schedule.every(self.__train_interval).days.do(self.retrainModel)

        #TODO: market exeception monitor, every 5 mints


    

        
