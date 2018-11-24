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


def check_decorator(check):
    """Decorator that provides the power for a check function
    to automatically decorates any function that returns a pd.DataFrame.

    The returned object will behave just like the check function but
    it provides an extra 'as_decorator' method that returns the according
    decorator.
    """
    class CheckDecorator:
        def __init__(self, check):
            self.check = check
            update_wrapper(self, check)

        def __call__(self, *args, **check_kwargs):
            return self.check(*args, **check_kwargs)

        def __repr__(self):
            return ("<function {module}.{function}{signature}>"
                    .format(module=self.__module__,
                            function=self.__name__,
                            signature=inspect.signature(self.check))
                    )

        def as_decorator(self, *check_args, **check_kwargs):
            @wraps(self.check)
            def func_wrapper(func):
                def args_wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    try:
                        self.check(result, *check_args, **check_kwargs)
                        return result
                    except AssertionError as e:
                        raise InvariantAssertionError(
                            ("Function '{function}' broke an invariant"
                             .format(function=func.__name__))) from e
                return args_wrapper
            return func_wrapper
    return CheckDecorator(check)


# ---------------
# Error reporting
# ---------------

def bad_locations(df):
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(1)]
    msg = bad.values
    return msg

__all__ = ['verify', 'verify_all', 'verify_any', 'bad_locations']
