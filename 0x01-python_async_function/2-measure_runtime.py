#!/usr/bin/env python3
""" 2-measure_runtime module """
import time
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ measure_time function """

    s = time.time()
    asyncio.run(wait_n(n, max_delay))
    return (time.time() - s) / n
