
def test_newton_complex_gh10103():
    # gh-10103 reported a problem when `newton` is pass a Python complex x0,
    # no `fprime` (secant method), and no `x1` (`x1` must be constructed).
    # Check that this is resolved.
    def f(z):
        return z - 1
    res = newton(f, 1+1j)
    assert_allclose(res, 1, atol=1e-12)

    res = root_scalar(f, x0=1+1j, x1=2+1.5j, method='secant')
    assert_allclose(res.root, 1, atol=1e-12)

