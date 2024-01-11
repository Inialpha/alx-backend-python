#!/usr/bin/env python3
""" module for element_length(lst) """
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ return length of lst """
    return [(i, len(i)) for i in lst]
