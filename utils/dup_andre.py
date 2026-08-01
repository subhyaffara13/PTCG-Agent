
def dup_andre(n, K):
    """Low-level implementation of Andre polynomials."""
    p = [K.one]
    for i in range(1, n+1):
        p = dup_integrate(dup_mul_ground(p, K(i), K), 1, K)
        if i % 2 == 0:
            p = dup_sub_ground(p, dup_eval(p, K.one, K), K)
    return p

