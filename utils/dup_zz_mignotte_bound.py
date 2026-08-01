
def dup_zz_mignotte_bound(f, K):
    """
    The Knuth-Cohen variant of Mignotte bound for
    univariate polynomials in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> f = x**3 + 14*x**2 + 56*x + 64
    >>> R.dup_zz_mignotte_bound(f)
    152

    By checking ``factor(f)`` we can see that max coeff is 8

    Also consider a case that ``f`` is irreducible for example
    ``f = 2*x**2 + 3*x + 4``. To avoid a bug for these cases, we return the
    bound plus the max coefficient of ``f``

    >>> f = 2*x**2 + 3*x + 4
    >>> R.dup_zz_mignotte_bound(f)
    6

    Lastly, to see the difference between the new and the old Mignotte bound
    consider the irreducible polynomial:

    >>> f = 87*x**7 + 4*x**6 + 80*x**5 + 17*x**4 + 9*x**3 + 12*x**2 + 49*x + 26
    >>> R.dup_zz_mignotte_bound(f)
    744

    The new Mignotte bound is 744 whereas the old one (SymPy 1.5.1) is 1937664.


    References
    ==========

    ..[1] [Abbott13]_

    """
    from sympy.functions.combinatorial.factorials import binomial
    d = dup_degree(f)
    delta = _ceil(d / 2)
    delta2 = _ceil(delta / 2)

    # euclidean-norm
    eucl_norm = K.sqrt( sum( cf**2 for cf in f ) )

    # biggest values of binomial coefficients (p. 538 of reference)
    t1 = binomial(delta - 1, delta2)
    t2 = binomial(delta - 1, delta2 - 1)

    lc = K.abs(dup_LC(f, K))   # leading coefficient
    bound = t1 * eucl_norm + t2 * lc   # (p. 538 of reference)
    bound += dup_max_norm(f, K) # add max coeff for irreducible polys
    bound = _ceil(bound / 2) * 2   # round up to even integer

    return bound

