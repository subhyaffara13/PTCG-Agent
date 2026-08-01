
def test_pmint_bessel_products():
    f = x*besselj(nu, x)*bessely(nu, 2*x)
    g = -2*x*besselj(nu, x)*bessely(nu - 1, 2*x)/3 + x*besselj(nu - 1, x)*bessely(nu, 2*x)/3

    assert heurisch(f, x) == g

    f = x*besselj(nu, x)*besselk(nu, 2*x)
    g = -2*x*besselj(nu, x)*besselk(nu - 1, 2*x)/5 - x*besselj(nu - 1, x)*besselk(nu, 2*x)/5

    assert heurisch(f, x) == g

