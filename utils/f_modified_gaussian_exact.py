import math


def f_modified_gaussian_exact(a, b, n, xp):
    # Exact only for the limits
    #   a = (0, 0, -oo, -oo)
    #   b = (1, oo, oo, oo)
    # but defined here as a function to match the format of the other integrands.
    return 1/(2 + 2*n) * math.pi ** (3/2)

