
def test_DifferentialExtension_misc():
    # Odd ends
    assert DifferentialExtension(sin(y)*exp(x), x)._important_attrs == \
        (Poly(sin(y)*t0, t0, domain='ZZ[sin(y)]'), Poly(1, t0, domain='ZZ'),
        [Poly(1, x, domain='ZZ'), Poly(t0, t0, domain='ZZ')], [x, t0],
        [Lambda(i, exp(i))], [], [None, 'exp'], [None, x])
    raises(NotImplementedError, lambda: DifferentialExtension(sin(x), x))
    assert DifferentialExtension(10**x, x)._important_attrs == \
        (Poly(t0, t0), Poly(1, t0), [Poly(1, x), Poly(log(10)*t0, t0)], [x, t0],
        [Lambda(i, exp(i*log(10)))], [(exp(x*log(10)), 10**x)], [None, 'exp'],
        [None, x*log(10)])
    assert DifferentialExtension(log(x) + log(x**2), x)._important_attrs in [
        (Poly(3*t0, t0), Poly(2, t0), [Poly(1, x), Poly(2/x, t0)], [x, t0],
        [Lambda(i, log(i**2))], [], [None, ], [], [1], [x**2]),
        (Poly(3*t0, t0), Poly(1, t0), [Poly(1, x), Poly(1/x, t0)], [x, t0],
        [Lambda(i, log(i))], [], [None, 'log'], [None, x])]
    assert DifferentialExtension(S.Zero, x)._important_attrs == \
        (Poly(0, x), Poly(1, x), [Poly(1, x)], [x], [], [], [None], [None])
    assert DifferentialExtension(tan(atan(x).rewrite(log)), x)._important_attrs == \
        (Poly(x, x), Poly(1, x), [Poly(1, x)], [x], [], [], [None], [None])

