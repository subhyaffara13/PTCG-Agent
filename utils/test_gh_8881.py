
def test_gh_8881():
    r"""Test that Halley's method realizes that the 2nd order adjustment
    is too big and drops off to the 1st order adjustment."""
    n = 9

    def f(x):
        return power(x, 1.0/n) - power(n, 1.0/n)

    def fp(x):
        return power(x, (1.0-n)/n)/n

    def fpp(x):
        return power(x, (1.0-2*n)/n) * (1.0/n) * (1.0-n)/n

    x0 = 0.1
    # The root is at x=9.
    # The function has positive slope, x0 < root.
    # Newton succeeds in 8 iterations
    rt, r = newton(f, x0, fprime=fp, full_output=True)
    assert r.converged
    # Before the Issue 8881/PR 8882, halley would send x in the wrong direction.
    # Check that it now succeeds.
    rt, r = newton(f, x0, fprime=fp, fprime2=fpp, full_output=True)
    assert r.converged

