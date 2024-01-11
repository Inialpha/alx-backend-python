#!/usr/bin/env python3
""" module for make_multiplier() """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    returns a function that multiplies a float by multiplier.
    """
    def mul(a: float) -> float:
        return multiplier * a
    return mul
