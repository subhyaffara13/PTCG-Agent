import sys
from typing import Callable

def skipIfOnlyNotPy312(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    if sys.version_info >= (3, 13) or sys.version_info < (3, 12):
        return unittest.skip("Requires Python 3.12")(fn)
    return fn

