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