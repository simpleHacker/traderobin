"""
concrete class provide method to get feeds from offline downloads
It is only used for one time training
bitcoinchats: https://bitcoincharts.com/about/markets-api/
"""

import csv
from datetime import datetime, timedelta
import gzip
import numpy as np
import io

import urllib
from pyalgotrade.bitcoincharts import barfeed
from pyalgotrade.tools import resample
from pyalgotrade import bar
from pyalgotrade.barfeed import csvfeed

import sys
sys.path.append(".")
import feeds

class BitcoinchartsFeeds(feeds.Feeds):
    COINBASE_HIST_URL = "http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
    CLOSE_INDEX = 4
    VOLUMN_INDEX = 5
    def __init__(self, datasource=COINBASE_HIST_URL):
        """
        download history gz file and unpack it
        save it on local dir. remove the old one everytime run this
        """
        response = urllib.request.urlopen(datasource)
        compressedFile = io.BytesIO(response.read())
        decompressedFile = gzip.GzipFile(fileobj=compressedFile)
        self._sourceFile = "bitcoin.csv"
        with open(self._sourceFile, 'wb') as outfile:
            outfile.write(decompressedFile.read())

    def get_resampled_file(self, symbol, interval, span):
        barFeed = barfeed.CSVTradeFeed()
        # from datetime should be one year away from today. always use one year window
        now = datetime.today()
        fromdate = now - timedelta(days=span)
        barFeed.addBarsFromCSV(self._sourceFile, fromDateTime=fromdate)
        outfilePath = "%smin-bitstampUSD.csv"%interval
        resample.resample_to_csv(barFeed, bar.Frequency.MINUTE*interval, outfilePath)
        return outfilePath

    def get_crypto_historicals(self, symbol, interval=5, span=30, bounds=""):
        outfilePath = self.get_resampled_file(symbol, interval, span)
        return getArray(outfilePath, self.CLOSE_INDEX)

    def get_crypto_historicals_vol(self, symbol, interval=5, span=30, bounds=""):
        outfilePath = self.get_resampled_file(symbol, interval, span)
        return getArray(outfilePath, self.VOLUMN_INDEX)

def getArray(filename, index):
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for row in reader:
            if not(row):
                continue
            yield (np.array(row[index], dtype=float))

if __name__ == "__main__":
    feeds = BitcoinchartsFeeds()
    itr = feeds.get_crypto_historicals("BTC")
    for price in itr:
        print(price)

    
