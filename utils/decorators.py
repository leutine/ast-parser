# coding: utf-8

import time

from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        before = time.perf_counter()
        result = func(*args, **kwargs)
        after = time.perf_counter()
        print(f"Func '{func.__name__}' execution: {after - before} s.")
        return result
    return wrapper


def get_element(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._get()
        result = func(*args, **kwargs)
        print("get_element decorator is done!")
        return result
    return wrapper
