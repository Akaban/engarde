# -*- coding: utf-8 -*-
"""
Module for useful generic functions.
"""
from itertools import chain, cycle
from functools import update_wrapper, wraps
import inspect

import numpy as np
import pandas as pd


# Exception

class InvariantAssertionError(AssertionError):
    def __init__(self, *args, input_dataframe=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_dataframe = input_dataframe

# Decorator

def as_decorator(check):
    """Decorator that provides the power for a check function to
    decorates any function that returns a pd.DataFrame
    """
    def check_wrapper(*check_args, **check_kwargs):
        @wraps(check)
        def func_wrapper(func):
            def args_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                try:
                    check(result, *check_args, **check_kwargs)
                    return result
                except AssertionError as e:
                    raise InvariantAssertionError(
                        ("Function '{function}' broke an invariant"
                         .format(function=func.__name__))) from e
            return args_wrapper
        return func_wrapper
    return check_wrapper


# Error reporting
# ---------------

def bad_locations(df):
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(1)]
    msg = bad.values
    return msg

__all__ = ['verify', 'verify_all', 'verify_any', 'bad_locations']
