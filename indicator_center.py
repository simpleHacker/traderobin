"""
* calulate each indicator from feeds
Indicators:
1. RSI, ({1y, 14p}, {1y, 5p}, {6m, 5p}, {1m, 6p}, {6m, 14p}, {1m, 14p})
2. Bollinger Bands:
3. MACD
4. On Balance Volume (OBV)
5. True Range (TR)
6. Average True Range (ATR)

* signal is optional. signal should be decided by trading strategy and model, not singly used
provide multiple signals on each indicator with signal type and value
Can have a global signal type table to check. so each indicator can report multiple signals

* operate as an in memory storage for different combination of calculation:
    - try find an efficient way to index combinations
    - find a way to serialize the map to file and read it back

* provide a chart drawing function

could use the same interface with same arguments passed in. but each chart define self data packing logic for func call!
"""

import datetime
import numpy as np
import sys
import shelve as sh
import tulipy as ti
# https://pypi.org/project/newtulipy/

from pathlib import Path
from . import feeds_robin as fr

class Indicators(object):
    """
    make it a abstract class and each indicator will implement it
    with indicator calculation and signal checkers
    start and end has to be unique, can not include each other!
    """
    # collection dict for all indicators, key as its name with param.
    
    def __init__(self, security, feeds, start, end):
        """
        take in feeds object
        """
        #TODO: define feeds structure!!
        self.__security = security
        self.__feeds = feeds
        self.__high = fr.get_high(self.__feeds)
        self.__low = fr.get_low(self.__feeds)
        self.__close = fr.get_close(self.__feeds)
        self.__id = security + ":" + start + "_" + end
        # update store by day
        self.__latest = datetime.date.now()
        self.__lock = False
        self.setDict(start, end)
        
        #TODO: shell we delete all data in shelve at the beginning???

    def setDict(self, security, start, end):
        DBFILE = "indicators.db" + "." + security + "." + start + "." + end
        shelfSavePath = Path(sys.argv[0]).parent / Path(DBFILE)
        self.ind_dict = sh.open(fr'{shelfSavePath}')


    def __del__(self):
        self.ind_dict.close()

    def __refresh(self, security, feeds, start, end):
        # close previos dict
        keys = self.ind_dict.keys()
        self.ind_dict.close()
        self.__feeds = feeds
        self.__high = fr.get_high(self.__feeds)
        self.__low = fr.get_low(self.__feeds)
        self.__close = fr.get_close(self.__feeds)
        self.__id = security + ":" + start + "_" + end
        self.setDict(security, start, end) # this will create a new shelf dict

        now = datetime.date.now()
        # delete old data and recalculate with new data, lock it when recalculate
        if now != self.__latest:
            self.__lock = True
            for k in keys:
                methd, params = self.dekey(k)
                method = getattr(self, methd.upper())
                method(*params)
    
    @staticmethod
    def key(l):
        re = '_'.join(str(e) for e in l)
        return re
    
    @staticmethod
    def dekey(k):
        re = k.split('_')
        params = [int(e) for e in re[1:]] if len(re) > 1 else []
        return re[0], params

    def RSI(self, period):
        """ Momentum
        take different span feeds to calculate period
        return one rsi array
        there is no two process update the same structure entry at the same time
        Every 5 mins (default), it will be calculated again
        @param feed (np.array, new tick), will be updated in 5min gap just the last added tick (no add in, just update)
        """
        self.ind_dict[self.key(["rsi",period])] = ti.rsi(self.__feeds, period)

    def BBands(self, period, stdev):
        """Trend Following
        default can use 20-period moving average, 2 multiply stdev.
        calculate per day.
        this indicator is used to assit other indicators, it does not give sell or buy signal directly.
        it tell the volitility potential for the market.
        return three bands: ['bbands_lower', 'bbands_middle', 'bbands_upper']
        """
        self.ind_dict[self.key(["bbands",period,stdev])] = ti.bbands(self.__feeds, period, stdev)

    def OBV(self, volume):
        self.ind_dict[self.key(["obv",volume])] = ti.obv(self.__feeds, volume)

    def MACD(self, short_period, long_period, signal_period):
        """Momentum
        """
        self.ind_dict[self.key(["macd", short_period, long_period, signal_period])] = ti.macd(self.__feeds, short_period, long_period, signal_period)

    # N day feeds - (low, high, close) arrays
    def TR(self):
        self.ind_dict["tr"] = ti.tr(self.__high, self.__low, self.__close)

    # N days feeds (low, high, close) arrays
    def ATR(self, period):
        # output a float
        self.ind_dict[self.key(["atr",period])] = ti.atr(self.__high, self.__low, self.__close, period)

    # directional indicator - positive, negtive
    def DI(self, period):
        # output: plus_di and minus_di array
        self.ind_dict[self.key(["plus_di", period])], self.ind_dict[("minus_di", period)] = ti.di(self.__high, self.__low, self.__close, period)

    def ADX(self, period):
        # output dx as float
        self.ind_dict[self.key(["adx", period])] = ti.adx(self.__high, self.__low, self.__close, period)

    def collectIndicators(self, inds, consts):
        # @param key, [(indicator_name, param_names array)...]
        # @param consts, {"param_name":param_value...}
        collect = {}
        for ind, par in inds:
            params = [consts[p] for p in par]
            key = self.key(ind, *params)
            if key in self.ind_dict:
                collect[ind] = self.ind_dict[key]
            else:
                print("Error: indicator=%s with key=%s is not exist" % (ind, key))
            return collect

    def signal_checker(self):
        pass

    def show(self, chart):
        pass

    


 ''' for RSI       
    def signal_checker(self, span, period):
        """
        use predefined selling and buying rules to filter current rsi value
        """
        rsi = self.ind_dict[(span, period)]
        # usually buy point is 30, sell point is 70
        # but here, we can use model trainer to get more accurate number
        # according to long term gain, using current trading strategy
        # when training them, give a range between 20-40 and 60-80
        # each trading strategy will get its own number (span, period) -> points
        #
        # after trainer recevied watch signal, it will trigger watch rules prepare to trade
        buy_point, sell_point = self.signal_points[(span, period)]
        if rsi[-1] < buy_point:
            watch_buy(); # combine strategy with trend or other signal
        elif rsi[-1] > sell_point:
            watch_sell(); # also combine

    # BBANDS:
    def signal_checker(self, span, period):
        """
        if close to the most narrow width, signal for preparation
        and check volitile.
        check up and low
        """
        upband, midband, lowband = self.ind_dict[(span, period)]
        if self.__feeds[-1] <= lowband[-1]:
        # check signal lowband penetrate
            diff = self.__feeds - lowband[-1]
            signal(BB_LOW, diff)
        elif self.__feeds[-1] >= upband[-1]:
        # check signal upband penetrate
            diff = self.__feeds[-1] - upband[-1]
            signal(BB_UP, diff)

        # check signal width, signal anyway    
        width = upband - lowband
        min_width = min(width)
        max_width = max(width)

        # for combination signal analysis
        if width == min_width:
            signal(BB_MIN_WIDTH)
        elif width == max_width:
            signal(BB_MAX_WIDTH)
        # if width without any change for a period, trade the band
        ## if feed[-1] >= upband[-2]: sell
        ## if feed[-1] <= lowband[-2]: buy

    def signal_checker(self, span):
        """
        signal when volumn climb or slip
        """
        obv = self.ind_dict[span]
        # when price climb as well
        if obv[-1] > obv[-1]:
            signal(OBV_UP)
        elif obv[-1] < obv[-1]:
            signal(OBV_DOWN)

'''

class Range(Indicator):
    # define all the constant
    def __init__(self, feeds):
        super().__init__(feeds)
        TIME_WINDOW = 3 # days
        UPPER = 1000 # can pick from recent historical, tag training set for best earning range
        LOWER = 100
        FREQUENCY = 3 # can pick from average earning sets
        MAX_SPAN = 2 # months, can train from risk model
    # return stable or instable, span should not longer than 
    def chart(self, feeds, span):
        starting_point = now - span # find calc start day
        ending_point = now - 1 # end at yesterday
        # range from 1 day to TIME_WINDOW for high and low
        (low, point_low) = find_min(starting_point, ending_point, feeds)
        (high, point_high) = find_max(starting_point, ending_point, feeds)
        lows.append((low,point_low))
        highs.append((high, point_high))
        sort_lows(lows)
        sort_highs(highs)
        
        # 3 lows has to distributed among 3 highs, need to calc distribution degree.
        # if two lows close to each other without have high in between, merge the two low to one low.
        # if two high close to each other without have low in between, also merge it.
        # 3 highs > 3 lows, then return it is a stable range, otherwise instable
        # train to find accuracy in term of n (3 low, high) 

        # strategy for trading
        # calc bband for the span on feeds
        # buy when market price close to lowerband + variance, sell when market price close to upperband - variance.
        # drop down the lowerband for a constant can be taken as leaving range pattern.
        # 
        # When use this model, better to also calculate trend and moving average, should not be down turn. 
        ## to decide on a upper trend: 1, plus_di >= minus_di; 2, adx >= 20 (can be trained according recent data)
        ## but use it need to be cautious, so train with historical data to find a proper adx for the strength.
