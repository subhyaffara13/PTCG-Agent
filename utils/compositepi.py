
def compositepi(n):
    """ Return the number of positive composite numbers less than or equal to n.
        The first positive composite is 4, i.e. compositepi(4) = 1.

        Examples
        ========

        >>> from sympy import compositepi
        >>> compositepi(25)
        15
        >>> compositepi(1000)
        831

        See Also
        ========

        sympy.ntheory.primetest.isprime : Test if n is prime
        primerange : Generate all primes in a given range
        prime : Return the nth prime
        primepi : Return the number of primes less than or equal to n
        composite : Return the nth composite number
    """
    n = int(n)
    if n < 4:
        return 0
    return n - _primepi(n) - 1

