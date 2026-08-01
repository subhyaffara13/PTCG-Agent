
def dup_bernoulli_c(n, K):
    """Low-level implementation of central Bernoulli polynomials."""
    p = [K.one]
    for i in range(1, n+1):
        p = dup_integrate(dup_mul_ground(p, K(i), K), 1, K)
        if i % 2 == 0:
            p = dup_sub_ground(p, dup_eval(p, K.one, K) * K((1<<(i-1))-1, (1<<i)-1), K)
    return p

