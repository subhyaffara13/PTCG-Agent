import math


def _rand_radius(rng, min_r, max_r):
    val = min_r - 1
    while val < min_r:
        val = math.sqrt(rng.random()) * max_r
    return val

