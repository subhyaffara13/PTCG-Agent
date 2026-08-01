
def test_laurent_series():
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1, t)]})
    a = Poly(36, t)
    d = Poly((t - 2)*(t**2 - 1)**2, t)
    F = Poly(t**2 - 1, t)
    n = 2
    assert laurent_series(a, d, F, n, DE) == \
        (Poly(-3*t**3 + 3*t**2 - 6*t - 8, t), Poly(t**5 + t**4 - 2*t**3 - 2*t**2 + t + 1, t),
        [Poly(-3*t**3 - 6*t**2, t, domain='QQ'), Poly(2*t**6 + 6*t**5 - 8*t**3, t, domain='QQ')])

