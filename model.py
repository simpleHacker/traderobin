"""
model platform to compose a model, and train on a strategy for different parameters

* one model instance is for one specific strategy to train all its instances
* add a strategy, load its indicators with a range of constants 
* exeute strategy with different valued indicators and constants for rules
* collect and save different running result with their parameters on training set
* test top performed parameterized strategy during training with latest test set
* save selected best performed strategy during testing
* feedback to the selected strategy with paper trade for a while for real performance
* training procedure is triggered by scheduler, and provide the best strategy for tradebot in each training cycle

"""

from indicator_center import Indicators

class model(object):

    def __init__(self, security, strategy, indicator_tags, constants_range):
        self.__security = security
        self.__strategy = strategy
        # indicator with param names in order
        self.__indicator_tags = indicator_tags
        self.__constants_range = constants_range
    
    #def loadStrategy(self, strategy):
    #    self.__strategy = strategy

    def permutator(self):
        k, v = self.__constants_range.popitem()
        interset = {}
        result = []
        def combine(key, value, rest, interset, result):
            if not key:
                result.append(interset.copy())
                return
            newKey = ''
            newValue = []
            tempset = rest.copy()
            if len(tempset) != 0:
                newkey, value = tempset.popitem()
            for i in value:
                interset[key] = i
                combine(newkey, newValue, tempset, interset, result)
                del interset[key]
        combine(k,v,self.__constants_range, interset, result)
        return result

    def calc_indicators(self, indicators, constants):
        # @param indicators, [(indicator_name, params_array)...]
        # @param constants, {'param_name':param_value...}
        # @param dataset, all the data collections
        # TODO: figure out start and end
        
        for ind, params in indicators:
            vec = []
            for p in params:
                vec.append(constants[p])
                func = getattr(self.__center, ind)
                func(**vec)

    # outside schedule manager to manage retrain everyday to recalculation
    def train(self, dataset, testset):
        # train to get optimal model that perform best, risk least
        # keep model, performance and risk data
        #TODO: check duplicate Indicators instance
        self.__center = Indicators(dataset['feeds'], 1, 2)
        #TODO: result should be indicator_tags and consts for rule as ID
        self.__results = {}
        constants = self.permutator() # {'N': (low, high, step), 'period': (5,14,1)...}
        order = None # init order, with all trade detail
        # can parallel
        for const in constants:
            self.calc_indicators(self.__indicator_tags, const)
            self.__strategy.loadIndicators(self.__indicator_tags, const, self.__center)
            # buy first
            for market in testset:
                if !order and self.__strategy.execute_buy(market):
                    priceA = testset["mark_price"]
                    #TODO: create order
                else order and self.__strategy.execute_sell(market):
                    #TODO: then sell order
                    priceB = testset["market_price"]
                if priceA > 0 and priceB > 0:
                    diff = priceB - priceA
                    self.__results[diff] = (self.__indicator_tags, const)
        pairs = self.findBest(3)
        paper_trade(pairs, feeds)
        # then use const to calc inds according to latest dataset, then rest of const as input to rule

    def electModel(self):
        key_list = list(self.__results.keys())
        best = max(key_list)
        self.__strategy.loadIndicators(best[0], best[1], self.__center)
        return self.__strategy



    def findBest(self, num):
        # find best num of return from result
        relist = list(self.__results.keys())
        relist.sort()
        bests = [self.__results[re] for re in relist]
        return bests

    def paper_trade(self, pairs, feeds):
        #for every 5 mins
        market = feeds.get_crypto_current(self.__security)
        self.__strategy.loadIndicators(pairs[0], pairs[1], self.__center)
        re1 = self.__strategy.execute_buy(market)
        re2 = self.__strategy.execute_sell(market)




    

