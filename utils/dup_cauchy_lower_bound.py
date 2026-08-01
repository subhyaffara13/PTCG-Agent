
def dup_cauchy_lower_bound(f, K):
    """Compute the Cauchy lower bound on the absolute value of all non-zero
       roots of f, real or complex."""
    g = dup_reverse(f)
    if len(g) < 2:
        raise PolynomialError('Polynomial has no non-zero roots.')
    if K.is_ZZ:
        K = K.get_field()
    b = dup_cauchy_upper_bound(g, K)
    return K.one / b

