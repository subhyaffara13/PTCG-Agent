import functools
from typing import Callable

def _keep_float(
    f: Callable[[Unpack[_Ts]], _T],
) -> Callable[[Unpack[_Ts]], _T | sympy.Float]:
    @functools.wraps(f)
    def inner(*args: Unpack[_Ts]) -> _T | sympy.Float:
        r: _T | sympy.Float = f(*args)
        if any(isinstance(a, sympy.Float) for a in args) and not isinstance(
            r, sympy.Float
        ):
            r = sympy.Float(float(r))
        return r

    # pyrefly: ignore [bad-return]
    return inner

