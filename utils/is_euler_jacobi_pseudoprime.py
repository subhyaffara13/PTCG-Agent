
def is_euler_jacobi_pseudoprime(n, a):
    r"""Returns True if ``n`` is prime or is an odd composite integer that
    is coprime to ``a`` and satisfy the modular arithmetic congruence relation:

    .. math ::
        a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod{n}

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
           The composite number that returns ``True`` is called an Euler-Jacobi pseudoprime.

    Examples
    ========

    >>> from sympy.ntheory.primetest import is_euler_jacobi_pseudoprime
    >>> from sympy.ntheory.factor_ import isprime
    >>> for n in range(1, 1000):
    ...     if is_euler_jacobi_pseudoprime(n, 2) and not isprime(n):
    ...         print(n)
    561

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Euler%E2%80%93Jacobi_pseudoprime
    """
    n, a = as_int(n), as_int(a)
    if a == 1:
        return n == 2 or bool(n % 2)
    return is_euler_prp(n, a)

