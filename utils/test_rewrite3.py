
def test_rewrite3():
    e = exp(-x + 1/x**2) - exp(x + 1/x)
    #both of these are correct and should be equivalent:
    assert mrewrite(mrv(e, x), x, m) in [(-1/m + m*exp(
        (x**2 + x)/x**3), -x - 1/x), ((m**2 - exp((x**2 + x)/x**3))/m, x**(-2) - x)]

