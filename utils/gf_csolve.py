
def gf_csolve(f, n):
    """
    To solve f(x) congruent 0 mod(n).

    n is divided into canonical factors and f(x) cong 0 mod(p**e) will be
    solved for each factor. Applying the Chinese Remainder Theorem to the
    results returns the final answers.

    Examples
    ========

    Solve [1, 1, 7] congruent 0 mod(189):

    >>> from sympy.polys.galoistools import gf_csolve
    >>> gf_csolve([1, 1, 7], 189)
    [13, 49, 76, 112, 139, 175]

    See Also
    ========

    sympy.ntheory.residue_ntheory.polynomial_congruence : a higher level solving routine

    References
    ==========

    .. [1] 'An introduction to the Theory of Numbers' 5th Edition by Ivan Niven,
           Zuckerman and Montgomery.

    """
    from sympy.polys.domains import ZZ
    from sympy.ntheory import factorint
    P = factorint(n)
    X = [csolve_prime(f, p, e) for p, e in P.items()]
    pools = list(map(tuple, X))
    perms = [[]]
    for pool in pools:
        perms = [x + [y] for x in perms for y in pool]
    dist_factors = [pow(p, e) for p, e in P.items()]
    return sorted([gf_crt(per, dist_factors, ZZ) for per in perms])

