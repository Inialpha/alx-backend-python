#!/usr/bin/env python3
""" asynchronous coroutine """
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """ the wait """
    r = random.uniform(0, max_delay)
    await asyncio.sleep(r)
    return r
