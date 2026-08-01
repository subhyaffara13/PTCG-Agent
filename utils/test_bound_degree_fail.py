
def test_bound_degree_fail():
    # Primitive
    DE = DifferentialExtension(extension={'D': [Poly(1, x),
        Poly(t0/x**2, t0), Poly(1/x, t)]})
    assert bound_degree(Poly(t**2, t), Poly(-(1/x**2*t**2 + 1/x), t),
        Poly((2*x - 1)*t**4 + (t0 + x)/x*t**3 - (t0 + 4*x**2)/2*x*t**2 + x*t,
        t), DE) == 3

