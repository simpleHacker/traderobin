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
        historical data - close price for train indicator
        for months data, directly get it online
        @return: close_price list
        """
        ''' example:
        >>> r.get_crypto_historicals("BTC","hour", "day")
        [{'begins_at': '2023-02-22T23:00:00Z', 'open_price': '24104.7679765179565', 'close_price': '24188.001673609631', 'high_price': '24228.636231825', 'low_price': '24082.90765575', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'},
        {'begins_at': '2023-02-23T00:00:00Z', 'open_price': '24188.001673609631', 'close_price': '24130.8941009600005', 'high_price': '24249.924840005', 'low_price': '24127.064837600001', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'}, 
        {'begins_at': '2023-02-23T01:00:00Z', 'open_price': '24131.01345841', 'close_price': '24191.54821742742', 'high_price': '24210.83242065', 'low_price': '24129.41762619757', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'}, 
        {'begins_at': '2023-02-23T02:00:00Z', 'open_price': '24191.54821742742', 'close_price': '24535.4057269012125', 'high_price': '24595.39423835', 'low_price': '24169.5927717', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'},
        {'begins_at': '2023-02-23T03:00:00Z', 'open_price': '24535.4057269012125', 'close_price': '24456.239806009999', 'high_price': '24602.4438711242135', 'low_price': '24435.600086675', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'},
        {'begins_at': '2023-02-23T04:00:00Z', 'open_price': '24456.239806009999', 'close_price': '24521.8307105699985', 'high_price': '24529.400087335', 'low_price': '24425.69576035', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'},
        {'begins_at': '2023-02-23T05:00:00Z', 'open_price': '24521.4071911299995', 'close_price': '24393.99737558', 'high_price': '24526.100089695', 'low_price': '24352.7391367300005', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'},
        {'begins_at': '2023-02-23T06:00:00Z', 'open_price': '24393.99737558', 'close_price': '24395.0180969976765', 'high_price': '24419.9221674', 'low_price': '24313.95197195', 'volume': 0, 'session': 'reg', 'interpolated': False, 'symbol': 'BTCUSD'}}
        '''

        hist = r.get_crypto_historicals(symbol, interval, span, bounds)
        return hist

    def get_closes(prices):
        return np.array([float(p['close_price']) for p in prices])

    def get_highs(prices):
        return np.array([float(p["high_price"]) for p in prices])

    def get_lows(prices):
        return np.array([float(p["low_price"]) for p in prices])


    def get_crypto_current(self, symbol):
        """
        {'ask_price': '13117.620352', 'bid_price': '13096.132242', 'mark_price': '13106.876297', 'high_price': '13236.045000', 
        'low_price': '12640.429462', 'open_price': '12770.175000', 'symbol': 'BTCUSD', 'id': '3d961844-d360-45fc-989b-f6fca761d511', 'volume': '0.000000'}
        @return: a tuple includes ask, bid, and mark
        """
        current = r.get_crypto_quote(symbol)
        return float(current['ask_price'], current['bid_price'], current['mark_price'])

    def prepare_training_data(self, symbol, interval="5minute", bounds="24_7"):
        """
        retrieve a year good data for training purpose
        for larger data only, like a year
        """
        if not self.HistoryData:
            self.HistoryData = r.get_crypto_historicals(symbol, interval, self.HistSpan, bounds)

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






    

    
