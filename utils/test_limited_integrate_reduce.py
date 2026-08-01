
def test_limited_integrate_reduce():
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)]})
    assert limited_integrate_reduce(Poly(x, t), Poly(t**2, t), [(Poly(x, t),
    Poly(t, t))], DE) == \
        (Poly(t, t), Poly(-1/x, t), Poly(t, t), 1, (Poly(x, t), Poly(1, t, domain='ZZ[x]')),
        [(Poly(-x*t, t), Poly(1, t, domain='ZZ[x]'))])

