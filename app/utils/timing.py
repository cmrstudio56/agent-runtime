import time
from contextlib import asynccontextmanager


class Timer:
    def __init__(self):
        self.start = None
        self.end = None

    def elapsed_ms(self):
        return int((self.end - self.start) * 1000)


@asynccontextmanager
async def async_timer():
    timer = Timer()
    timer.start = time.time()
    try:
        yield timer
    finally:
        timer.end = time.time()
