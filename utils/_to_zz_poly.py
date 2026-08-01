
def _to_ZZ_poly(f, ring):
    r"""
    Compute an associate of a polynomial
    `f \in \mathbb Q(\alpha)[x_0, \ldots, x_{n-1}]` in
    `\mathbb Z[x_1, \ldots, x_{n-1}][z] / (\check m_{\alpha}(z))[x_0]`,
    where `\check m_{\alpha}(z) \in \mathbb Z[z]` is the primitive associate
    of the minimal polynomial `m_{\alpha}(z)` of `\alpha` over
    `\mathbb Q`.

    Parameters
    ==========

    f : PolyElement
        polynomial in `\mathbb Q(\alpha)[x_0, \ldots, x_{n-1}]`
    ring : PolyRing
        `\mathbb Z[x_1, \ldots, x_{n-1}][x_0, z]`

    Returns
    =======

    f_ : PolyElement
        associate of `f` in
        `\mathbb Z[x_1, \ldots, x_{n-1}][x_0, z]`

    """
    f_ = ring.zero

    if isinstance(ring.domain, PolynomialRing):
        domain = ring.domain.domain
    else:
        domain = ring.domain

    den = domain.one

    for coeff in f.itercoeffs():
        for c in coeff.to_list():
            if c:
                den = domain.lcm(den, c.denominator)

    for monom, coeff in f.iterterms():
        coeff = coeff.to_list()
        m = ring.domain.one
        if isinstance(ring.domain, PolynomialRing):
            m = m.mul_monom(monom[1:])
        n = len(coeff)

        for i in range(n):
            if coeff[i]:
                c = domain.convert(coeff[i] * den) * m

                if (monom[0], n-i-1) not in f_:
                    f_[(monom[0], n-i-1)] = c
                else:
                    f_[(monom[0], n-i-1)] += c

    return f_

