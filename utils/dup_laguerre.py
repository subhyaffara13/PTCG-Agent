
def dup_laguerre(n, alpha, K):
    """Low-level implementation of Laguerre polynomials."""
    m2, m1 = [K.zero], [K.one]
    for i in range(1, n+1):
        a = dup_mul(m1, [-K.one/K(i), (alpha-K.one)/K(i) + K(2)], K)
        b = dup_mul_ground(m2, (alpha-K.one)/K(i) + K.one, K)
        m2, m1 = m1, dup_sub(a, b, K)
    return m1

