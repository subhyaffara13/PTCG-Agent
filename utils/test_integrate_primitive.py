
def test_integrate_primitive():
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)],
        'Tfuncs': [log]})
    assert integrate_primitive(Poly(t, t), Poly(1, t), DE) == (x*log(x), -1, True)
    assert integrate_primitive(Poly(x, t), Poly(t, t), DE) == (0, NonElementaryIntegral(x/log(x), x), False)

    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t1), Poly(1/(x + 1), t2)],
        'Tfuncs': [log, Lambda(i, log(i + 1))]})
    assert integrate_primitive(Poly(t1, t2), Poly(t2, t2), DE) == \
        (0, NonElementaryIntegral(log(x)/log(1 + x), x), False)

    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t1), Poly(1/(x*t1), t2)],
        'Tfuncs': [log, Lambda(i, log(log(i)))]})
    assert integrate_primitive(Poly(t2, t2), Poly(t1, t2), DE) == \
        (0, NonElementaryIntegral(log(log(x))/log(x), x), False)

    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t0)],
        'Tfuncs': [log]})
    assert integrate_primitive(Poly(x**2*t0**3 + (3*x**2 + x)*t0**2 + (3*x**2
    + 2*x)*t0 + x**2 + x, t0), Poly(x**2*t0**4 + 4*x**2*t0**3 + 6*x**2*t0**2 +
    4*x**2*t0 + x**2, t0), DE) == \
        (-1/(log(x) + 1), NonElementaryIntegral(1/(log(x) + 1), x), False)

