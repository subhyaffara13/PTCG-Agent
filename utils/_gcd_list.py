import functools
import math


def _gcd_list(numbers: Sequence[int]) -> int:
    return 0 if not numbers else functools.reduce(math.gcd, numbers)

