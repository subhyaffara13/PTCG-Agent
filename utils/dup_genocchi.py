
def dup_genocchi(n, K):
    """Low-level implementation of Genocchi polynomials."""
    if n < 1:
        return [K.zero]
    p = [-K.one]
    for i in range(2, n+1):
        p = dup_integrate(dup_mul_ground(p, K(i), K), 1, K)
        if i % 2 == 0:
            p = dup_sub_ground(p, dup_eval(p, K.one, K) // K(2), K)
    return p

