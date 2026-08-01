
def dup_hermite_prob(n, K):
    """Low-level implementation of probabilist's Hermite polynomials."""
    if n < 1:
        return [K.one]
    m2, m1 = [K.one], [K.one, K.zero]
    for i in range(2, n+1):
        a = dup_lshift(m1, 1, K)
        b = dup_mul_ground(m2, K(i-1), K)
        m2, m1 = m1, dup_sub(a, b, K)
    return m1

