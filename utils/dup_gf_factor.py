
def dup_gf_factor(f, K):
    """Factor univariate polynomials over finite fields. """
    f = dup_convert(f, K, K.dom)

    coeff, factors = gf_factor(f, K.mod, K.dom)

    for i, (f, k) in enumerate(factors):
        factors[i] = (dup_convert(f, K.dom, K), k)

    return K.convert(coeff, K.dom), factors

