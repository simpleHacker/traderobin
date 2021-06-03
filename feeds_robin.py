"""
concrete class provide method to get feeds from robin
"""

import sys
sys.path.append(".")
import feeds
import numpy as np
import robin_stocks as r
from datetime import datetime

class RobinFeeds(feeds.Feeds):

    HistoryData = []
    HistSpan="year"
    Symbol="BTC"
    fromDatetime = datetime.today()

    def __init__(self, histSpan):
        self.set_hist_span(histSpan)
        self.prepare_training_data(self.Symbol)

    def get_crypto_historicals(self, symbol, interval="5minute", span="year", bounds="24_7"):
        """
        historical data for train indicator
        for months data, directly get it online
        @return: close_price list
        """
        hist = r.crypto.get_crypto_historicals(symbol, interval, span, bounds, "close_price")
        return np.array(hist)

    def get_crypto_current(self, symbol):
        """
        {'ask_price': '13117.620352', 'bid_price': '13096.132242', 'mark_price': '13106.876297', 'high_price': '13236.045000', 
        'low_price': '12640.429462', 'open_price': '12770.175000', 'symbol': 'BTCUSD', 'id': '3d961844-d360-45fc-989b-f6fca761d511', 'volume': '0.000000'}
        @return: a tuple includes ask, bid, and mark
        """
        current = r.crypto.get_crypto_quote(symbol)
        return float(current['ask_price'], current['bid_price'], current['mark_price'])

    def prepare_training_data(self, symbol, interval="5minute", bounds="24_7"):
        """
        retrieve a year good data for training purpose
        for larger data only, like a year
        """
        if not self.HistoryData:
            self.HistoryData = r.crypto.get_crypto_historicals(symbol, interval, self.HistSpan, bounds)

    def get_half_data(self):
        half = len(self.HistoryData)/2
        return self.HistoryData[half:]

    def get_data_from(self, date):
        """
        get data from base data set from the 'date'
        """
        

    def set_hist_span(self, span):
        """
        for changing databsae longest span
        """
        self.HistSpan = span






    

    
