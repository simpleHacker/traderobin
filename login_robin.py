"""
concrete class provide method to login in robin
"""

from . import login
import pyotp
import robin_stocks.robinhood as r

class RobinLogin(login.Login):
    def login(self, account, passwd, options="", token=""):
        if options == "2FA" and token:
            totp = pyotp.TOTP(token).now()
            lg = r.login(account, passwd, mfa_code=totp)
        else:
            lg = r.login(account, passwd)    
