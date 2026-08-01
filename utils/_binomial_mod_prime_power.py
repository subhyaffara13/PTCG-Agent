
def _binomial_mod_prime_power(n, m, p, q):
    """Compute ``binomial(n, m) % p**q`` for a prime ``p``.

    Parameters
    ==========

    n : positive integer
    m : a nonnegative integer
    p : a prime
    q : a positive integer (the prime exponent)

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _binomial_mod_prime_power
    >>> _binomial_mod_prime_power(10, 2, 3, 2)  # binomial(10, 2) = 45
    0
    >>> _binomial_mod_prime_power(17, 9, 2, 4)  # binomial(17, 9) = 24310
    6

    References
    ==========

    .. [1] Binomial coefficients modulo prime powers, Andrew Granville,
        Available: https://web.archive.org/web/20170202003812/http://www.dms.umontreal.ca/~andrew/PDF/BinCoeff.pdf
    """
    # Function/variable naming within this function follows Ref.[1]
    # n!_p will be used to denote the product of integers <= n not divisible by
    # p, with binomial(n, m)_p the same as binomial(n, m), but defined using
    # n!_p in place of n!
    modulo = pow(p, q)

    def up_factorial(u):
        """Compute (u*p)!_p modulo p^q."""
        r = q // 2
        fac = prod = 1
        if r == 1 and p == 2 or 2*r + 1 in (p, p*p):
            if q % 2 == 1: r += 1
            modulo, div = pow(p, 2*r), pow(p, 2*r - q)
        else:
            modulo, div = pow(p, 2*r + 1), pow(p, (2*r + 1) - q)
        for j in range(1, r + 1):
            for mul in range((j - 1)*p + 1, j*p):  # ignore jp itself
                fac *= mul
                fac %= modulo
            bj_ = bj(u, j, r)
            prod *= pow(fac, bj_, modulo)
            prod %= modulo
        if p == 2:
            sm = u // 2
            for j in range(1, r + 1): sm += j//2 * bj(u, j, r)
            if sm % 2 == 1: prod *= -1
        prod %= modulo//div
        return prod % modulo

    def bj(u, j, r):
        """Compute the exponent of (j*p)!_p in the calculation of (u*p)!_p."""
        prod = u
        for i in range(1, r + 1):
            if i != j: prod *= u*u - i*i
        for i in range(1, r + 1):
            if i != j: prod //= j*j - i*i
        return prod // j

    def up_plus_v_binom(u, v):
        """Compute binomial(u*p + v, v)_p modulo p^q."""
        prod = 1
        div = invert(factorial(v), modulo)
        for j in range(1, q):
            b = div
            for v_ in range(j*p + 1, j*p + v + 1):
                b *= v_
                b %= modulo
            aj = u
            for i in range(1, q):
                if i != j: aj *= u - i
            for i in range(1, q):
                if i != j: aj //= j - i
            aj //= j
            prod *= pow(b, aj, modulo)
            prod %= modulo
        return prod

    @recurrence_memo([1])
    def factorial(v, prev):
        """Compute v! modulo p^q."""
        return v*prev[-1] % modulo

    def factorial_p(n):
        """Compute n!_p modulo p^q."""
        u, v = divmod(n, p)
        return (factorial(v) * up_factorial(u) * up_plus_v_binom(u, v)) % modulo

    prod = 1
    Nj, Mj, Rj = n, m, n - m
    # e0 will be the p-adic valuation of binomial(n, m) at p
    e0 = carry = eq_1 = j = 0
    while Nj:
        numerator = factorial_p(Nj % modulo)
        denominator = factorial_p(Mj % modulo) * factorial_p(Rj % modulo) % modulo
        Nj, (Mj, mj), (Rj, rj) = Nj//p, divmod(Mj, p), divmod(Rj, p)
        carry = (mj + rj + carry) // p
        e0 += carry
        if j >= q - 1: eq_1 += carry
        prod *= numerator * invert(denominator, modulo)
        prod %= modulo
        j += 1

    mul = pow(1 if p == 2 and q >= 3 else -1, eq_1, modulo)
    return (pow(p, e0, modulo) * mul * prod) % modulo

