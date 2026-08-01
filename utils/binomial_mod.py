
def binomial_mod(n, m, k):
    """Compute ``binomial(n, m) % k``.

    Explanation
    ===========

    Returns ``binomial(n, m) % k`` using a generalization of Lucas'
    Theorem for prime powers given by Granville [1]_, in conjunction with
    the Chinese Remainder Theorem.  The residue for each prime power
    is calculated in time O(log^2(n) + q^4*log(n)log(p) + q^4*p*log^3(p)).

    Parameters
    ==========

    n : an integer
    m : an integer
    k : a positive integer

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import binomial_mod
    >>> binomial_mod(10, 2, 6)  # binomial(10, 2) = 45
    3
    >>> binomial_mod(17, 9, 10)  # binomial(17, 9) = 24310
    0

    References
    ==========

    .. [1] Binomial coefficients modulo prime powers, Andrew Granville,
        Available: https://web.archive.org/web/20170202003812/http://www.dms.umontreal.ca/~andrew/PDF/BinCoeff.pdf
    """
    if k < 1: raise ValueError('k is required to be positive')
    # We decompose q into a product of prime powers and apply
    # the generalization of Lucas' Theorem given by Granville
    # to obtain binomial(n, k) mod p^e, and then use the Chinese
    # Remainder Theorem to obtain the result mod q
    if n < 0 or m < 0 or m > n: return 0
    factorisation = factorint(k)
    residues = [_binomial_mod_prime_power(n, m, p, e) for p, e in factorisation.items()]
    return crt([p**pw for p, pw in factorisation.items()], residues, check=False)[0]

