from . import contextlib, io, sys

class DummyStream(io.StringIO):
    def write(self, s):
        return len(s)
    def flush(self):
        pass

@contextlib.contextmanager
from utils.silence_kaggle_warnings import silence_kaggle_warnings

