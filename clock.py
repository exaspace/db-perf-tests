import time


class Clock:

    def __init__(self, desc, start=False):
        self.desc = desc
        self.t1 = None
        self.t2 = None
        self.count = None
        if start:
            self.start()

    def start(self):
        assert self.t1 is None
        self.t1 = time.time()

    def stop(self):
        assert self.t2 is None
        self.t2 = time.time()

    def report(self, count):
        secs = self.t2 - self.t1
        rate = count/secs if secs > 0 else 0
        print(f"{self.desc}\t{round(rate, 1)} per second ({count} in {round(secs, 1)} seconds)")

    def stop_and_report(self, count):
        self.stop()
        self.count = count
        self.report(count)


class Timer:

    def __init__(self, desc):
        self.main_desc = desc
        self.clocks = []

    def start_phase(self, desc):
        clock = Clock(f'{self.main_desc}\t{desc}', start=True)
        self.clocks.append(clock)

    def stop_phase(self, count):
        self.clocks[-1].stop_and_report(count)
