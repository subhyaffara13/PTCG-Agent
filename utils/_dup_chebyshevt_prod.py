
def _dup_chebyshevt_prod(n, K):
    r""" Chebyshev polynomials of the first kind using recursive products.

    Explanation
    ===========

    Computes Chebyshev polynomials of the first kind using

    .. math::
        T_{2n}(x) &= 2T_n^2(x) - 1\\
        T_{2n+1}(x) &= 2T_{n+1}(x)T_n(x) - x

    This is faster than ``_dup_chebyshevt_rec`` for large ``n``.

    Parameters
    ==========

    n : int
        n is a nonnegative integer.
    K : domain

    """
    m2, m1 = [K.one, K.zero], [K(2), K.zero, -K.one]
    for i in bin(n)[3:]:
        c = dup_sub_term(dup_mul_ground(dup_mul(m1, m2, K), K(2), K), K.one, 1, K)
        if  i  == '1':
            m2, m1 = c, dup_sub_ground(dup_mul_ground(dup_sqr(m1, K), K(2), K), K.one, K)
        else:
            m2, m1 = dup_sub_ground(dup_mul_ground(dup_sqr(m2, K), K(2), K), K.one, K), c
    return m2

