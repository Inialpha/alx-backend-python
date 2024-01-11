#!/usr/bin/env python3
""" module to_kv() """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ returns a tuple: (k, v²) """

    return (k, v * v)
