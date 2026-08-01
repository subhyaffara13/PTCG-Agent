
def dup_cauchy_upper_bound(f, K):
    """
    Compute the Cauchy upper bound on the absolute value of all roots of f,
    real or complex.

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Geometrical_properties_of_polynomial_roots#Lagrange's_and_Cauchy's_bounds
    """
    n = dup_degree(f)
    if n < 1:
        raise PolynomialError('Polynomial has no roots.')

    if K.is_ZZ:
        L = K.get_field()
        f, K = dup_convert(f, K, L), L
    elif not K.is_QQ or K.is_RR or K.is_CC:
        # We need to compute absolute value, and we are not supporting cases
        # where this would take us outside the domain (or its quotient field).
        raise DomainError('Cauchy bound not supported over %s' % K)
    else:
        f = f[:]

    while K.is_zero(f[-1]):
        f.pop()
    if len(f) == 1:
        # Monomial. All roots are zero.
        return K.zero

    lc = f[0]
    return K.one + max(abs(n / lc) for n in f[1:])

