import math


def assoc_legendre_factor(n, m, norm):
    if norm:
        return (math.sqrt((2 * n + 1) *
            math.factorial(n - m) / (2 * math.factorial(n + m))))

    return 1

