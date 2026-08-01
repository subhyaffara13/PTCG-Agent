
def prime_valuation(I, P):
    r"""
    Compute the *P*-adic valuation for an integral ideal *I*.

    Examples
    ========

    >>> from sympy import QQ
    >>> from sympy.polys.numberfields import prime_valuation
    >>> K = QQ.cyclotomic_field(5)
    >>> P = K.primes_above(5)
    >>> ZK = K.maximal_order()
    >>> print(prime_valuation(25*ZK, P[0]))
    8

    Parameters
    ==========

    I : :py:class:`~.Submodule`
        An integral ideal whose valuation is desired.

    P : :py:class:`~.PrimeIdeal`
        The prime at which to compute the valuation.

    Returns
    =======

    int

    See Also
    ========

    .PrimeIdeal.valuation

    References
    ==========

    .. [1] Cohen, H. *A Course in Computational Algebraic Number Theory.*
       (See Algorithm 4.8.17.)

    """
    p, ZK = P.p, P.ZK
    n, W, d = ZK.n, ZK.matrix, ZK.denom

    A = W.convert_to(QQ).inv() * I.matrix * d / I.denom
    # Although A must have integer entries, given that I is an integral ideal,
    # as a DomainMatrix it will still be over QQ, so we convert back:
    A = A.convert_to(ZZ)
    D = A.det()
    if D % p != 0:
        return 0

    beta = P.test_factor()

    f = d ** n // W.det()
    need_complete_test = (f % p == 0)
    v = 0
    while True:
        # Entering the loop, the cols of A represent lin combs of omegas.
        # Turn them into lin combs of thetas:
        A = W * A
        # And then one column at a time...
        for j in range(n):
            c = ZK.parent(A[:, j], denom=d)
            c *= beta
            # ...turn back into lin combs of omegas, after multiplying by beta:
            c = ZK.represent(c).flat()
            for i in range(n):
                A[i, j] = c[i]
        if A[n - 1, n - 1].element % p != 0:
            break
        A = A / p
        # As noted above, domain converts to QQ even when division goes evenly.
        # So must convert back, even when we don't "need_complete_test".
        if need_complete_test:
            # In this case, having a non-integer entry is actually just our
            # halting condition.
            try:
                A = A.convert_to(ZZ)
            except CoercionFailed:
                break
        else:
            # In this case theory says we should not have any non-integer entries.
            A = A.convert_to(ZZ)
        v += 1
    return v

