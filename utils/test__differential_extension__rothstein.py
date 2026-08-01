
def test_DifferentialExtension_Rothstein():
    # Rothstein's integral
    f = (2581284541*exp(x) + 1757211400)/(39916800*exp(3*x) +
    119750400*exp(x)**2 + 119750400*exp(x) + 39916800)*exp(1/(exp(x) + 1) - 10*x)
    assert DifferentialExtension(f, x)._important_attrs == \
        (Poly((1757211400 + 2581284541*t0)*t1, t1), Poly(39916800 +
        119750400*t0 + 119750400*t0**2 + 39916800*t0**3, t1),
        [Poly(1, x), Poly(t0, t0), Poly(-(10 + 21*t0 + 10*t0**2)/(1 + 2*t0 +
        t0**2)*t1, t1, domain='ZZ(t0)')], [x, t0, t1],
        [Lambda(i, exp(i)), Lambda(i, exp(1/(t0 + 1) - 10*i))], [],
        [None, 'exp', 'exp'], [None, x, 1/(t0 + 1) - 10*x])

