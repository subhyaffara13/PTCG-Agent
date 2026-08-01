
def is_euler_pseudoprime(n, a):
    r"""Returns True if ``n`` is prime or is an odd composite integer that
    is coprime to ``a`` and satisfy the modular arithmetic congruence relation:

    .. math ::
        a^{(n-1)/2} \equiv \pm 1 \pmod{n}

    (where mod refers to the modulo operation).

    Parameters
    ==========

    n : Integer
        ``n`` is a positive integer.
    a : Integer
        ``a`` is a positive integer.
        ``a`` and ``n`` should be relatively prime.

    Returns
    =======

    bool : If ``n`` is prime, it always returns ``True``.
           The composite number that returns ``True`` is called an Euler pseudoprime.

    Examples
    ========

    >>> from sympy.ntheory.primetest import is_euler_pseudoprime
    >>> from sympy.ntheory.factor_ import isprime
    >>> for n in range(1, 1000):
    ...     if is_euler_pseudoprime(n, 2) and not isprime(n):
    ...         print(n)
    341
    561

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Euler_pseudoprime
    """
    n, a = as_int(n), as_int(a)
    if a < 1:
        raise ValueError("a should be an integer greater than 0")
    if n < 1:
        raise ValueError("n should be an integer greater than 0")
    if n == 1:
        return False
    if a == 1:
        return n == 2 or bool(n % 2)  # (prime or odd composite)
    if n % 2 == 0:
        return n == 2
    if gcd(n, a) != 1:
        raise ValueError("The two numbers should be relatively prime")
    return pow(a, (n - 1) // 2, n) in [1, n - 1]

