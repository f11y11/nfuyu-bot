import logging
from time import time

__all__ = (
    'Timer',
)


class Timer:
    """
    Provides context managers that measure the time elapsed since __aenter__
    :return: Timer
    """
    def __init__(self, name: str = None):
        self.name = name
        self._start = 0
        self._stop = 0

    def __aenter__(self, *args, **kwargs):
        self._start = time()
        return self

    def __aexit__(self, *args, **kwargs):
        self._stop = time()
        if self.name:
            logging.info(f'Timer {self.name} resulted with: {self.result:.2f}')

    @property
    def result(self):
        return self._stop - self._start
