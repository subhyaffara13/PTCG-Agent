
def test_yule_simon():
    from sympy.core.singleton import S
    rho = S(3)
    x = YuleSimon('x', rho)
    assert simplify(E(x)) == rho / (rho - 1)
    assert simplify(variance(x)) == rho**2 / ((rho - 1)**2 * (rho - 2))
    assert isinstance(E(x, evaluate=False), Expectation)
    # To test the cdf function
    assert cdf(x)(x) == Piecewise((-beta(floor(x), 4)*floor(x) + 1, x >= 1), (0, True))

