from typing import Any

def as_mpmath(x: Any, prec: int, options: OPT_DICT) -> mpc | mpf:
    from .numbers import Infinity, NegativeInfinity, Zero
    x = sympify(x)
    if isinstance(x, Zero) or x == 0.0:
        return mpf(0)
    if isinstance(x, Infinity):
        return mpf('inf')
    if isinstance(x, NegativeInfinity):
        return mpf('-inf')
    # XXX
    result = evalf(x, prec, options)
    return quad_to_mpmath(result)

