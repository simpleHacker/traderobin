import time
import schedule
import model
import sys
import shelve as sh
from pathlib import Path


class TradeController(object):
    
    def __init__(self, time_config) -> None:
        self.__feeds_interval = time_config["feeds"]
        self.__ind_interval = time_config["indicator"]
        self.__train_interval = time_config["model"]
        self._setOMS();

    def _setOMS(self):
        DBFILE = "oms.db"
        shelfSavePath = Path(sys.argv[0]).parent / Path(DBFILE)
        self.__OMS = sh.open(fr'{shelfSavePath}')

    # only use when model already exist, usually start from createModel
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
    
    def createModel(self, security, strategy, indicator_tags, constants_range):
        self.__model = model.Model(security, strategy, indicator_tags, constants_range)

    def trainModel(self, history):
        dataset, testset = self.prepareDataset(history)
        self.__model.train(dataset, testset)
        self.__strategy = self.__model.elect()

    def callMarket(self, ticker, market):
        result = self.__strategy.executeBuy(market)
        if eval(self.__buyRule, {}, {"signal":result, "oms":self.__OMS}):
            self.createOsrder(ticker, market, "BL") # buy limit on the market to move

    def putMarket(self, ticker, market):
        result = self.__strategy.executeSell(market)
        if eval(self.__sellRule, {}, {'signal':result, "oms":self.__OMS}):
            self.createOrder(ticker, market, "SL") # sell limit on the market to move

    def createOrder(self, market_price, order_type):
        # at very beginning, there's not too many orders, so just need to persistent on local disks for recovery
        # also update order status in OMS
        pass

# OMS: orderId, parseKey, quantity, price, status, sell-buy diff (new, filled, cancelled = deleted)




    def trade(self, market):
        # according to trade rule, select how many shares to trade (with certain risk)
        # if trade rule allowed, run callMarket
        # if rule allowed and holding exist, according to trade rule, run putMarket


        

    def scheduler(self):
        schedule.every(self.__feeds_interval).minutes.do(self.getFeeds)
        schedule.every(self.__ind_interval).minutes.do(self.recalIndicator)
        schedule.every(self.__train_interval).days.do(self.retrainModel)

    def run(self):
        

        #TODO: market exeception monitor, every 5 mints

    def workflow(self):
        pass

    

        
