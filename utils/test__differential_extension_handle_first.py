
def test_DifferentialExtension_handle_first():
    assert DifferentialExtension(exp(x)*log(x), x, handle_first='log')._important_attrs == \
        (Poly(t0*t1, t1), Poly(1, t1), [Poly(1, x), Poly(1/x, t0),
        Poly(t1, t1)], [x, t0, t1], [Lambda(i, log(i)), Lambda(i, exp(i))],
        [], [None, 'log', 'exp'], [None, x, x])
    assert DifferentialExtension(exp(x)*log(x), x, handle_first='exp')._important_attrs == \
        (Poly(t0*t1, t1), Poly(1, t1), [Poly(1, x), Poly(t0, t0),
        Poly(1/x, t1)], [x, t0, t1], [Lambda(i, exp(i)), Lambda(i, log(i))],
        [], [None, 'exp', 'log'], [None, x, x])

    # This one must have the log first, regardless of what we set it to
    # (because the log is inside of the exponential: x**x == exp(x*log(x)))
    assert DifferentialExtension(-x**x*log(x)**2 + x**x - x**x/x, x,
    handle_first='exp')._important_attrs == \
        DifferentialExtension(-x**x*log(x)**2 + x**x - x**x/x, x,
        handle_first='log')._important_attrs == \
        (Poly((-1 + x - x*t0**2)*t1, t1), Poly(x, t1),
            [Poly(1, x), Poly(1/x, t0), Poly((1 + t0)*t1, t1)], [x, t0, t1],
            [Lambda(i, log(i)), Lambda(i, exp(t0*i))], [(exp(x*log(x)), x**x)],
            [None, 'log', 'exp'], [None, x, t0*x])

