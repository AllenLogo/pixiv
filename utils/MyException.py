# -*- coding:utf-8 -*-

from functools import wraps

def raiseException(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                raise Exception("[%s]:%s" % (func.__name__, error))
            else:
                return result
    return wrapper

class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)