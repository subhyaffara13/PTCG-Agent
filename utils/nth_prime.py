
def nth_prime(n, *, approximate=False):
    """Return the nth prime (counting from 0).

    >>> nth_prime(0)
    2
    >>> nth_prime(100)
    547

    If *approximate* is set to True, will return a prime close
    to the nth prime.  The estimation is much faster than computing
    an exact result.

    >>> nth_prime(200_000_000, approximate=True)  # Exact result is 4222234763
    4217820427

    """
    lb, ub = _nth_prime_bounds(n + 1)

    if not approximate or n <= 1_000_000:
        return nth(sieve(ceil(ub)), n)

    # Search from the midpoint and return the first odd prime
    odd = floor((lb + ub) / 2) | 1
    return first_true(count(odd, step=2), pred=is_prime)

