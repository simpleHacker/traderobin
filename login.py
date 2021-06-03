"""
generic class login to give generic method interface
different trading platform can inherit this class to define their own login in
"""

from abc import ABC, abstractclassmethod

class Login(ABC):

    @abstractclassmethod
    def login(self, account, passwd, option=""):
        pass