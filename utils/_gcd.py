import math


def _gcd(a, b):
    """Calculate the greatest common divisor of a and b"""
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError('Can only find greatest common divisor of '
                         f'finite arguments, found "{a}" and "{b}"')
    while b:
        a, b = b, a % b
    return a

