
def roots_cyclotomic(f, factor=False):
    """Compute roots of cyclotomic polynomials. """
    L, U = _inv_totient_estimate(f.degree())

    for n in range(L, U + 1):
        g = cyclotomic_poly(n, f.gen, polys=True)

        if f.expr == g.expr:
            break
    else:  # pragma: no cover
        raise RuntimeError("failed to find index of a cyclotomic polynomial")

    roots = []

    if not factor:
        # get the indices in the right order so the computed
        # roots will be sorted
        h = n//2
        ks = [i for i in range(1, n + 1) if igcd(i, n) == 1]
        ks.sort(key=lambda x: (x, -1) if x <= h else (abs(x - n), 1))
        d = 2*I*pi/n
        for k in reversed(ks):
            roots.append(exp(k*d).expand(complex=True))
    else:
        g = Poly(f, extension=root(-1, n))

        for h, _ in ordered(g.factor_list()[1]):
            roots.append(-h.TC())

    return roots

