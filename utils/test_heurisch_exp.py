
def test_heurisch_exp():
    assert heurisch(exp(x), x) == exp(x)
    assert heurisch(exp(-x), x) == -exp(-x)
    assert heurisch(exp(17*x), x) == exp(17*x) / 17
    assert heurisch(x*exp(x), x) == x*exp(x) - exp(x)
    assert heurisch(x*exp(x**2), x) == exp(x**2) / 2

    assert heurisch(exp(-x**2), x) is None

    assert heurisch(2**x, x) == 2**x/log(2)
    assert heurisch(x*2**x, x) == x*2**x/log(2) - 2**x*log(2)**(-2)

    assert heurisch(Integral(x**z*y, (y, 1, 2), (z, 2, 3)).function, x) == (x*x**z*y)/(z+1)
    assert heurisch(Sum(x**z, (z, 1, 2)).function, z) == x**z/log(x)

    # https://github.com/sympy/sympy/issues/23707
    anti = -exp(z)/(sqrt(x - y)*exp(z*sqrt(x - y)) - exp(z*sqrt(x - y)))
    assert heurisch(exp(z)*exp(-z*sqrt(x - y)), z) == anti

