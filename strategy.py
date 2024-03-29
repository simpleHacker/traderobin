"""
strategy platform to make different strategy and execute, so different strategy instances 
is represented by loaded rule with valued indicators and rule condition constants

* make different strategies that can load different indicators and constant and rules
* can execute loaded rule with given indicators and constants.
* dynamicly execute with pass-in market data
* 


# easy to add new strategies
# can try and store different parameters for different model  
"""

from asyncio.proactor_events import _ProactorBaseWritePipeTransport

from indicator_center import Indicators


class Strategy(object):
    # for each specific strategy, need to register parameter list for rule evaluation
    def __init__(self, rule):
        
        # @rule, rule string for eval
        self.__rule = rule
    
    def loadIndicators(self, inds, consts, center):
        # strategy load in indicators dynamically
        # @indicators, indicator with its value {'unique_ind_name':value}
        # @const, const name value {'N': value,...}
        # this indicators are calculated one as np array
        self.__indicators = center.collectIndicators(inds, consts)

    def execute_buy(self, market):
        # run the strategy - keep running
        # @market, {current_price, current_close, previous_close}
        # evaluate the rule expression when new tick coming 
        params = {**self.__indicators, **self.__const, **market}
        result = eval(self.__buy_rule, {}, params)
        return result

    def execute_sell(self, market):
        params = {**self.__indicators, **self.__const, **market}
        result = eval(self.__sell_rule, {}, params)
        return result
        

    def loadRule(self, rule):
        # load the rule expression from file 
        ## when to buy
        ## when to sell
        ## and how to buy and sell
        pass



    def updateInd(self, indicators):
        # receive update of all indicator calculations
        # get call every time when some params has new value in
        self.__indicators = indicators

    def loadParameters(self, indicator, const):
        self.__indicators = indicator
        self.__const = const

    def kill(self):
        # kill switch to kill the strategy
        pass

