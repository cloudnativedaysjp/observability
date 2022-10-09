import math
from datetime import datetime
from typing import Callable

import numpy as np


class SimpleQueue:
    period_seconds: int

    _q: list[int]
    _prev_tick: datetime
    _force_reset_period: int

    def __init__(self, period_seconds: int):
        self.period_seconds = period_seconds
        self._force_reset_period = period_seconds * 2
        self._q = []
        self._prev_tick = datetime.now()

    def add(self, count: int):
        self._q.append(count)

    def reset(self):
        self._q.clear()
        self._prev_tick = datetime.now()

    def run_after_period(self, fn: Callable[[list[int]], bool]):
        now = datetime.now()
        delta = now - self._prev_tick
        if delta.seconds < self.period_seconds:
            return
        print(f"{now} - {self._q}")
        ok = fn(self._q)

        if ok or delta.seconds > self._force_reset_period:
            self.reset()
