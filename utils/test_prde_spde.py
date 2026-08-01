
def test_prde_spde():
    D = [Poly(x, t), Poly(-x*t, t)]
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)]})
    # TODO: when bound_degree() can handle this, test degree bound from that too
    assert prde_spde(Poly(t, t), Poly(-1/x, t), D, n, DE) == \
        (Poly(t, t), Poly(0, t, domain='ZZ(x)'),
        [Poly(2*x, t, domain='ZZ(x)'), Poly(-x, t, domain='ZZ(x)')],
        [Poly(-x**2, t, domain='ZZ(x)'), Poly(0, t, domain='ZZ(x)')], n - 1)

