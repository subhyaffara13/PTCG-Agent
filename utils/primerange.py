
def primerange(a, b=None):
    """ Generate a list of all prime numbers in the range [2, a),
        or [a, b).

        If the range exists in the default sieve, the values will
        be returned from there; otherwise values will be returned
        but will not modify the sieve.

        Examples
        ========

        >>> from sympy import primerange, prime

        All primes less than 19:

        >>> list(primerange(19))
        [2, 3, 5, 7, 11, 13, 17]

        All primes greater than or equal to 7 and less than 19:

        >>> list(primerange(7, 19))
        [7, 11, 13, 17]

        All primes through the 10th prime

        >>> list(primerange(prime(10) + 1))
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        The Sieve method, primerange, is generally faster but it will
        occupy more memory as the sieve stores values. The default
        instance of Sieve, named sieve, can be used:

        >>> from sympy import sieve
        >>> list(sieve.primerange(1, 30))
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        Notes
        =====

        Some famous conjectures about the occurrence of primes in a given
        range are [1]:

        - Twin primes: though often not, the following will give 2 primes
                    an infinite number of times:
                        primerange(6*n - 1, 6*n + 2)
        - Legendre's: the following always yields at least one prime
                        primerange(n**2, (n+1)**2+1)
        - Bertrand's (proven): there is always a prime in the range
                        primerange(n, 2*n)
        - Brocard's: there are at least four primes in the range
                        primerange(prime(n)**2, prime(n+1)**2)

        The average gap between primes is log(n) [2]; the gap between
        primes can be arbitrarily large since sequences of composite
        numbers are arbitrarily large, e.g. the numbers in the sequence
        n! + 2, n! + 3 ... n! + n are all composite.

        See Also
        ========

        prime : Return the nth prime
        nextprime : Return the ith prime greater than n
        prevprime : Return the largest prime smaller than n
        randprime : Returns a random prime in a given range
        primorial : Returns the product of primes based on condition
        Sieve.primerange : return range from already computed primes
                           or extend the sieve to contain the requested
                           range.

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Prime_number
        .. [2] https://primes.utm.edu/notes/gaps.html
    """
    if b is None:
        a, b = 2, a
    if a >= b:
        return
    # If we already have the range, return it.
    largest_known_prime = sieve._list[-1]
    if b <= largest_known_prime:
        yield from sieve.primerange(a, b)
        return
    # If we know some of it, return it.
    if a <= largest_known_prime:
        yield from sieve._list[bisect_left(sieve._list, a):]
        a = largest_known_prime + 1
    elif a % 2:
        a -= 1
    tail = min(b, (largest_known_prime)**2)
    if a < tail:
        yield from sieve._primerange(a, tail)
        a = tail
    if b <= a:
        return
    # otherwise compute, without storing, the desired range.
    while 1:
        a = nextprime(a)
        if a < b:
            yield a
        else:
            return

