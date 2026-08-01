
def dmp_zz_wang_lead_coeffs(f, T, cs, E, H, A, u, K):
    """Wang/EEZ: Compute correct leading coefficients. """
    C, J, v = [], [0]*len(E), u - 1

    for h in H:
        c = dmp_one(v, K)
        d = dup_LC(h, K)*cs

        for i in reversed(range(len(E))):
            k, e, (t, _) = 0, E[i], T[i]

            while not (d % e):
                d, k = d//e, k + 1

            if k != 0:
                c, J[i] = dmp_mul(c, dmp_pow(t, k, v, K), v, K), 1

        C.append(c)

    if not all(J):
        raise ExtraneousFactors  # pragma: no cover

    CC, HH = [], []

    for c, h in zip(C, H):
        d = dmp_eval_tail(c, A, v, K)
        lc = dup_LC(h, K)

        if K.is_one(cs):
            cc = lc//d
        else:
            g = K.gcd(lc, d)
            d, cc = d//g, lc//g
            h, cs = dup_mul_ground(h, d, K), cs//d

        c = dmp_mul_ground(c, cc, v, K)

        CC.append(c)
        HH.append(h)

    if K.is_one(cs):
        return f, HH, CC

    CCC, HHH = [], []

    for c, h in zip(CC, HH):
        CCC.append(dmp_mul_ground(c, cs, v, K))
        HHH.append(dmp_mul_ground(h, cs, 0, K))

    f = dmp_mul_ground(f, cs**(len(H) - 1), u, K)

    return f, HHH, CCC

