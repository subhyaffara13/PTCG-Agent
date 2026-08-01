
def test_pmint_besselj():
    f = besselj(nu + 1, x)/besselj(nu, x)
    g = nu*log(x) - log(besselj(nu, x))

    assert heurisch(f, x) == g

    f = (nu*besselj(nu, x) - x*besselj(nu + 1, x))/x
    g = besselj(nu, x)

    assert heurisch(f, x) == g

    f = jn(nu + 1, x)/jn(nu, x)
    g = nu*log(x) - log(jn(nu, x))

    assert heurisch(f, x) == g

