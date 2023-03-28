"""
Bot take the whole workflow of trading

Description:
 1) login
 2) get market data - feeder
 3) indicator calculator
 4) trading model trainer
 5) signal generator
 6) trade executor

Usage:
    python tradingbot.py -u <userId> -p <passwd> -i <uinfo> [-e]

Options:
    -u <userId>     user name
    -p <passwd>     password
    -i <uinfo>      uinfo
    -e              execution mode

"""

import docopt
import pyotp
from . import login_robin
import robin_stocks as r

def login(uinfo, options):
    with open(uinfo, "r") as f:
        lines = [line for line in f]
        logi = r.login(lines[0], lines[1], options, lines[2])
    return logi

def main(argv):
    userId = None
    passwd = None
    uinfo = None
    isExecution = False
    options=""


    # parse in all parameters
    if argv["-u"]:
        userId = argv["-u"]
    else:
        print("Error: No userId")
        return
    if argv["-p"]:
        passwd = argv["-p"]
    else:
        print("Error: No password")
        return
    if argv["-i"]:
        uinfo = argv["-i"]
        options= "2FA"
    else:
        print("Error: No info")
        return
    if argv["-e"]:
        isExecution = True
    
    # workflow
    ## login
    lginfo = login(uinfo, options)
    print(lginfo)

    ##TODO take in hist and real time market data into feeds
    #build_feeds()
    #get_market_data()
    # - get histry: robin_stocks.stocks.get_stock_historicals()
    # - get current: robin_stocks.stocks.get_latest_price()
    # - all basic info: robin_stocks.stocks.get_fundamentals()
    #registor feeder, and start
    # - history feeder to provide certain range of market data in batch way or streaming way
    # - real time feeder to get real time market data

    ##TODO calculate all indicators according to feeds data
    #load_indicators() - subscribe to feeders and start listen
    #calc_indicators() - in preset range of params - in a separate thread

    ##TODO train or load the models from indicator and trading rules - in a separate thread
    #load indicator trading rules
    #train the model with diff combo of indicators in diff param range, find the best params and combo
    #save the model
    #trigger indicator recaculate and model re-training every X period (hours, day) - in a separate thread

    ##TODO monitor real time feeds in model and send signal - in a separate thread
    # model listen to realtime feeds
    # send out signal when model get trigered

    ##TODO executor - infinite loop on a variable -- main thread
    # listen to model signals, when received signal, alert to me in email or message.
    # if auto trade enabled, executed according to signal, and record the execution in db

    ##TODO signal a program from outside to set stop variable
    # join all the threads
    # r.logout()













