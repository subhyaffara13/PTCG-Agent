import math


def _divisor_sigma(n:int, k:int=1) -> int:
    r""" Calculate the divisor function `\sigma_k(n)` for positive integer n

    Parameters
    ==========

    n : int
        positive integer
    k : int
        nonnegative integer

    See Also
    ========

    sympy.functions.combinatorial.numbers.divisor_sigma

    """
    if k == 0:
        return math.prod(e + 1 for e in factorint(n).values())
    return math.prod((p**(k*(e + 1)) - 1)//(p**k - 1) for p, e in factorint(n).items())

