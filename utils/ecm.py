
def ecm(n, B1=10000, B2=100000, max_curve=200, seed=1234):
    """Performs factorization using Lenstra's Elliptic curve method.

    This function repeatedly calls ``_ecm_one_factor`` to compute the factors
    of n. First all the small factors are taken out using trial division.
    Then ``_ecm_one_factor`` is used to compute one factor at a time.

    Parameters
    ==========

    n : Number to be Factored
    B1 : Stage 1 Bound. Must be an even number.
    B2 : Stage 2 Bound. Must be an even number.
    max_curve : Maximum number of curves generated
    seed : Initialize pseudorandom generator

    Examples
    ========

    >>> from sympy.ntheory import ecm
    >>> ecm(25645121643901801)
    {5394769, 4753701529}
    >>> ecm(9804659461513846513)
    {4641991, 2112166839943}
    """
    from .factor_ import _perfect_power
    n = as_int(n)
    if B1 % 2 != 0 or B2 % 2 != 0:
        raise ValueError("both bounds must be even")
    TF_LIMIT = 100000
    factors = set()
    for prime in sieve.primerange(2, TF_LIMIT):
        if n % prime == 0:
            factors.add(prime)
            while(n % prime == 0):
                n //= prime

    queue = []
    def check(m):
        if isprime(m):
            factors.add(m)
            return
        if result := _perfect_power(m, TF_LIMIT):
            return check(result[0])
        queue.append(m)
    check(n)
    while queue:
        n = queue.pop()
        factor = _ecm_one_factor(n, B1, B2, max_curve, seed)
        if factor is None:
            raise ValueError("Increase the bounds")
        check(factor)
        check(n // factor)
    return factors

