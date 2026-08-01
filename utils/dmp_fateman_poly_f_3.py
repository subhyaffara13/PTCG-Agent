
def dmp_fateman_poly_F_3(n, K):
    """Fateman's GCD benchmark: sparse inputs (deg f ~ vars f) """
    u = dup_from_raw_dict({n + 1: K.one}, K)

    for i in range(0, n - 1):
        u = dmp_add_term([u], dmp_one(i, K), n + 1, i + 1, K)

    v = dmp_add_term(u, dmp_ground(K(2), n - 2), 0, n, K)

    f = dmp_sqr(
        dmp_add_term([dmp_neg(v, n - 1, K)], dmp_one(n - 1, K), n + 1, n, K), n, K)
    g = dmp_sqr(dmp_add_term([v], dmp_one(n - 1, K), n + 1, n, K), n, K)

    v = dmp_add_term(u, dmp_one(n - 2, K), 0, n - 1, K)

    h = dmp_sqr(dmp_add_term([v], dmp_one(n - 1, K), n + 1, n, K), n, K)

    return dmp_mul(f, h, n, K), dmp_mul(g, h, n, K), h

