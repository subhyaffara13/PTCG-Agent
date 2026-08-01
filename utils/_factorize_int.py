
def _factorize_int(n):
    """Return a sorted list of the unique prime factors of a positive integer.
    """
    # NOTE: There are lots faster ways to do this, but this isn't terrible.
    factors = set()
    for p in primes_from_2_to(int(np.sqrt(n)) + 1):
        while not (n % p):
            factors.add(p)
            n //= p
        if n == 1:
            break
    if n != 1:
        factors.add(n)
    return sorted(factors)

