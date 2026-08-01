
def prime(nth):
    r"""
    Return the nth prime number, where primes are indexed starting from 1:
    prime(1) = 2, prime(2) = 3, etc.

    Parameters
    ==========

    nth : int
        The position of the prime number to return (must be a positive integer).

    Returns
    =======

    int
        The nth prime number.

    Examples
    ========

    >>> from sympy import prime
    >>> prime(10)
    29
    >>> prime(1)
    2
    >>> prime(100000)
    1299709

    See Also
    ========

    sympy.ntheory.primetest.isprime : Test if a number is prime.
    primerange : Generate all primes in a given range.
    primepi : Return the number of primes less than or equal to a given number.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Prime_number_theorem
    .. [2] https://en.wikipedia.org/wiki/Logarithmic_integral_function
    .. [3] https://en.wikipedia.org/wiki/Skewes%27_number
    """
    n = as_int(nth)
    if n < 1:
        raise ValueError("nth must be a positive integer; prime(1) == 2")

    # Check if n is within the sieve range
    if n <= len(sieve._list):
        return sieve[n]

    from sympy.functions.elementary.exponential import log
    from sympy.functions.special.error_functions import li

    if n < 1000:
        # Extend sieve up to 8*n as this is empirically sufficient
        sieve.extend(8 * n)
        return sieve[n]

    a = 2
    # Estimate an upper bound for the nth prime using the prime number theorem
    b = int(n * (log(n).evalf() + log(log(n)).evalf()))

    # Binary search for the least m such that li(m) > n
    while a < b:
        mid = (a + b) >> 1
        if li(mid).evalf() > n:
            b = mid
        else:
            a = mid + 1

    return nextprime(a - 1, n - _primepi(a - 1))

