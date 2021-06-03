"""
concrete class provide method to login in robin
"""

from . import login
import pyotp
import robin_stocks as r

class RobinLogin(Login):
    def login(self, account, passwd, options=""):
        # totp = pyotp.TOTP("").now()
        lg = r.login(account, passwd)
        #lg = r.login(account, passwd, mfa_code=totp)       
