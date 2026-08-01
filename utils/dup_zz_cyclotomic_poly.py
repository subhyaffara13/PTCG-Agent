
def dup_zz_cyclotomic_poly(n, K):
    """Efficiently generate n-th cyclotomic polynomial. """
    from sympy.ntheory import factorint
    h = [K.one, -K.one]

    for p, k in factorint(n).items():
        h = dup_quo(dup_inflate(h, p, K), h, K)
        h = dup_inflate(h, p**(k - 1), K)

    return h

