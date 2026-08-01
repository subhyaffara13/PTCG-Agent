
def is_prime(n):
    """Return ``True`` if *n* is prime and ``False`` otherwise.

    Basic examples:

        >>> is_prime(37)
        True
        >>> is_prime(3 * 13)
        False
        >>> is_prime(18_446_744_073_709_551_557)
        True

    Find the next prime over one billion:

        >>> next(filter(is_prime, count(10**9)))
        1000000007

    Generate random primes up to 200 bits and up to 60 decimal digits:

        >>> from random import seed, randrange, getrandbits
        >>> seed(18675309)

        >>> next(filter(is_prime, map(getrandbits, repeat(200))))
        893303929355758292373272075469392561129886005037663238028407

        >>> next(filter(is_prime, map(randrange, repeat(10**60))))
        269638077304026462407872868003560484232362454342414618963649

    This function is exact for values of *n* below 10**24.  For larger inputs,
    the probabilistic Miller-Rabin primality test has a less than 1 in 2**128
    chance of a false positive.
    """

    if n < 17:
        return n in {2, 3, 5, 7, 11, 13}

    if not (n & 1 and n % 3 and n % 5 and n % 7 and n % 11 and n % 13):
        return False

    for limit, bases in _perfect_tests:
        if n < limit:
            break
    else:
        bases = (_private_randrange(2, n - 1) for i in range(64))

    return all(_strong_probable_prime(n, base) for base in bases)

