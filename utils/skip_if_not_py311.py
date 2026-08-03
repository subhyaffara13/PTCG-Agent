import sys
from typing import Callable

def skipIfNotPy311(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    if sys.version_info >= (3, 11):
        return fn
    # pyrefly: ignore [bad-return, bad-argument-type]
    return unittest.skip(fn)

