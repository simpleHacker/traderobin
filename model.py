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

    def __init__(self, strategy, indicator_tags, constants_range, dataset):
        self.__strategy = strategy
        # indicator with param names in order
        self.__indicator_tags = indicator_tags
        self.__constants_range = constants_range
        self.__dataset = dataset
        #TODO: delete start and end
        self.__center = Indicators(dataset, 1, 2)

    def loadStrategy(self, strategy):
        self.__strategy = strategy

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
        self.__ind_instance = Indicators(dataset['feeds'], 1, 2)
        self.__ind_instance.reload(dataset['feeds'], dataset['high'], dataset['low'], dataset['close'])
        for ind, params in indicators:
            vec = []
            for p in params:
                vec.append(constants[p]) 
                func = getattr(self.__ind_instance, ind)
                func(**vec)

    def train(self, dataset, testset):
        #TODO: this strategy should belongs to model class
        # train to get optimal model that perform best, risk least
        # keep model, performance and risk data
        constants = self.permutator() # {'N': (low, high, step), 'period': (5,14,1)...}
        # can parallel
        for const in constants:
            self.calc_indicators(self.__indicator_tags, const, dataset)
            self.__strategy.loadIndicators(self.__indicator_tags, const, self.__center)
            for market in testset:
                self.__strategy.execute(market)
            diff = self.__strategy.report()
            store(inds, const, diff)
        const = findBest(store_map)
        paper_trade(strategy, constant)
        # then use const to calc inds according to latest dataset, then rest of const as input to rule


    

