"""
calulate each indicator from feeds
Indicators:
1. RSI, ({1y, 14p}, {1y, 5p}, {6m, 5p}, {1m, 6p}, {6m, 14p}, {1m, 14p})
2. Bollinger Bands:
3. MACD
4. On Balance Volume (OBV)

provide multiple signals on each indicator with signal type and value
Can have a global signal type table to check. so each indicator can report multiple signals
"""

import numpy as np
import tulipy as ti

class Indicator(object):
    """
    make it a abstract class and each indicator will implement it
    with indicator calculation and signal checkers
    """
    # collection dict for all indicators, key as its name with param.
    self.ind_dict = dict()
    def __init__(self, feeds):
        """
        take in feeds object
        """
        self.__feeds = feeds

    def chart(self, period):
        pass

    def signal_checker(self):
        pass

    def show(self):
        pass

class RSI(Indicator):
    """
    Every 5 mins (default), it will be calculated again
    """
    self.signal_points= dict() # training task will set signal_points

    def chart(self, feed, span, period):
        """ Momentum
        take different span feeds to calculate period
        return one rsi array
        there is no two process update the same structure entry at the same time
        @param feed (np.array, new tick), will be updated in 5min gap just the last added tick (no add in, just update)
        """
        self.ind_dict[(span, period)] = ti.rsi(feed, period)

    def show(self, span, period):
        

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

class BBands(Indicator):
    """
    default can use 20-period moving average, 2 multiply stdev.
    calculate per day.
    this indicator is used to assit other indicators, it does not give sell or buy signal directly.
    it tell the volitility potential for the market.
    """
    signal_points = dict() # training task will set signal_points

    def chart(self, feed, span, period, stdev):
        """Trend Following
        return three bands: ['bbands_lower', 'bbands_middle', 'bbands_upper']
        """
        self.ind_dict[(span, period)] = ti.bbands(feed, period, stddev)
        # calculate bandwidth

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

    def show(self, span, period):

class OBV(Indicator):

    def chart(self, feeds, span, volumn):
        """momentum
        use to compbine with RSI and BBands to confirm trading decisions.
        usually this is not used during day
        return an array of obvs
        """
        self.ind_dict[span] = ti.obv(feeds, volume)

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

    def show(self, span):

class MACD(Indicator):

    
    def macd(self, feed=self.__feeds, short_period, long_period, signal_period):
        """Momentum
        """
        return ti.macd(feed, short_period, long_period, signal_period):