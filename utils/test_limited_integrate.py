
def test_limited_integrate():
    DE = DifferentialExtension(extension={'D': [Poly(1, x)]})
    G = [(Poly(x, x), Poly(x + 1, x))]
    assert limited_integrate(Poly(-(1 + x + 5*x**2 - 3*x**3), x),
    Poly(1 - x - x**2 + x**3, x), G, DE) == \
        ((Poly(x**2 - x + 2, x), Poly(x - 1, x, domain='QQ')), [2])
    G = [(Poly(1, x), Poly(x, x))]
    assert limited_integrate(Poly(5*x**2, x), Poly(3, x), G, DE) == \
        ((Poly(5*x**3/9, x), Poly(1, x, domain='QQ')), [0])

