
def test_DifferentialExtension_symlog():
    # See comment on test_risch_integrate below
    assert DifferentialExtension(log(x**x), x)._important_attrs == \
        (Poly(t0*x, t1), Poly(1, t1), [Poly(1, x), Poly(1/x, t0), Poly((t0 +
            1)*t1, t1)], [x, t0, t1], [Lambda(i, log(i)), Lambda(i, exp(i*t0))],
            [(exp(x*log(x)), x**x)], [None, 'log', 'exp'], [None, x, t0*x])
    assert DifferentialExtension(log(x**y), x)._important_attrs == \
        (Poly(y*t0, t0), Poly(1, t0), [Poly(1, x), Poly(1/x, t0)], [x, t0],
        [Lambda(i, log(i))], [(y*log(x), log(x**y))], [None, 'log'],
        [None, x])
    assert DifferentialExtension(log(sqrt(x)), x)._important_attrs == \
        (Poly(t0, t0), Poly(2, t0), [Poly(1, x), Poly(1/x, t0)], [x, t0],
        [Lambda(i, log(i))], [(log(x)/2, log(sqrt(x)))], [None, 'log'],
        [None, x])

