
def test_integrate_hypertangent_polynomial():
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t**2 + 1, t)]})
    assert integrate_hypertangent_polynomial(Poly(t**2 + x*t + 1, t), DE) == \
        (Poly(t, t), Poly(x/2, t))
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(a*(t**2 + 1), t)]})
    assert integrate_hypertangent_polynomial(Poly(t**5, t), DE) == \
        (Poly(1/(4*a)*t**4 - 1/(2*a)*t**2, t), Poly(1/(2*a), t))

