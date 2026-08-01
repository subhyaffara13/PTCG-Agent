
def test_polynomial_reduce():
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1 + t**2, t)]})
    assert polynomial_reduce(Poly(1 + x*t + t**2, t), DE) == \
        (Poly(t, t), Poly(x*t, t))
    assert polynomial_reduce(Poly(0, t), DE) == \
        (Poly(0, t), Poly(0, t))

