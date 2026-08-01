
def _check_smoothness(num, factor_base):
    r""" Check if `num` is smooth with respect to the given `factor_base`
    and compute its factorization vector.

    Parameters
    ==========

    num : integer whose smootheness is to be checked
    factor_base : factor_base primes
    """
    if num < 0:
        num *= -1
        vec = 1
    else:
        vec = 0
    for i, fb in enumerate(factor_base, 1):
        if num % fb.prime:
            continue
        e = 1
        num //= fb.prime
        while num % fb.prime == 0:
            e += 1
            num //= fb.prime
        if e % 2:
            vec += 1 << i
    return vec, num

