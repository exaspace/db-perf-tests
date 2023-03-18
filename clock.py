import time
import sys
from typing import Sequence


class Clock:

    def __init__(self, desc, start=False):
        self.desc = desc
        self.t1 = None
        self.t2 = None
        self.count = None
        if start:
            self.start()

    def start(self) -> None:
        assert self.t1 is None
        self.t1 = time.time()

    def stop(self, count: int) -> None:
        assert self.t2 is None
        self.t2 = time.time()
        self.count = count

    def secs(self) -> int:
        assert self.t2 is not None
        return self.t2 - self.t1

    def rate(self):
        return round(self.count / self.secs(), 2) if self.secs() > 0 else 0


class Timer:

    def __init__(self, desc: str):
        self.desc = desc
        self.clocks: Sequence[Clock] = []

    def start_phase(self, desc: str):
        clock = Clock(desc, start=True)
        self.clocks.append(clock)

    def stop_phase(self, count: int):
        clock = self.clocks[-1]
        clock.stop(count)
        self.report(clock)

    def report(self, c: Clock):
        sys.stderr.write(
            f"{self.desc}\t{c.desc}\t{c.rate()} per second ({c.count} in {round(c.secs(), 1)} seconds)\n")

