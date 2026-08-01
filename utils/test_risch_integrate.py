
def test_risch_integrate():
    assert risch_integrate(t0*exp(x), x) == t0*exp(x)
    assert risch_integrate(sin(x), x, rewrite_complex=True) == -exp(I*x)/2 - exp(-I*x)/2

    # From my GSoC writeup
    assert risch_integrate((1 + 2*x**2 + x**4 + 2*x**3*exp(2*x**2))/
    (x**4*exp(x**2) + 2*x**2*exp(x**2) + exp(x**2)), x) == \
        NonElementaryIntegral(exp(-x**2), x) + exp(x**2)/(1 + x**2)


    assert risch_integrate(0, x) == 0

    # also tests prde_cancel()
    e1 = log(x/exp(x) + 1)
    ans1 = risch_integrate(e1, x)
    assert ans1 == (x*log(x*exp(-x) + 1) + NonElementaryIntegral((x**2 - x)/(x + exp(x)), x))
    assert cancel(diff(ans1, x) - e1) == 0

    # also tests issue #10798
    e2 = (log(-1/y)/2 - log(1/y)/2)/y - (log(1 - 1/y)/2 - log(1 + 1/y)/2)/y
    ans2 = risch_integrate(e2, y)
    assert ans2 == log(1/y)*log(1 - 1/y)/2 - log(1/y)*log(1 + 1/y)/2 + \
            NonElementaryIntegral((I*pi*y**2 - 2*y*log(1/y) - I*pi)/(2*y**3 - 2*y), y)
    assert expand_log(cancel(diff(ans2, y) - e2), force=True) == 0

    # These are tested here in addition to in test_DifferentialExtension above
    # (symlogs) to test that backsubs works correctly.  The integrals should be
    # written in terms of the original logarithms in the integrands.

    # XXX: Unfortunately, making backsubs work on this one is a little
    # trickier, because x**x is converted to exp(x*log(x)), and so log(x**x)
    # is converted to x*log(x). (x**2*log(x)).subs(x*log(x), log(x**x)) is
    # smart enough, the issue is that these splits happen at different places
    # in the algorithm.  Maybe a heuristic is in order
    assert risch_integrate(log(x**x), x) == x**2*log(x)/2 - x**2/4

    assert risch_integrate(log(x**y), x) == x*log(x**y) - x*y
    assert risch_integrate(log(sqrt(x)), x) == x*log(sqrt(x)) - x/2

