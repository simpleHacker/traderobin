"""
interface to take in and aggregate feeds from different source
"""

from abc import ABC, abstractclassmethod

class Feeds(object):

    @abstractclassmethod
    def get_crypto_historicals(self, symbol, interval, span, bounds):
        pass

    @abstractclassmethod
    def get_crypto_current(self, symbol):
        pass