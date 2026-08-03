import math


def _cospi_real(x):
    if x < 0:
        x = -x
    n, r = divmod(x, 0.5)
    r *= pi
    n %= 4
    if n == 0: return math.cos(r)
    if n == 1: return -math.sin(r)
    if n == 2: return -math.cos(r)
    if n == 3: return math.sin(r)

