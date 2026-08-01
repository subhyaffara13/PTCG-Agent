
def test_precomputed_cdf():
    x = symbols("x", real=True)
    mu = symbols("mu", real=True)
    sigma, xm, alpha = symbols("sigma xm alpha", positive=True)
    n = symbols("n", integer=True, positive=True)
    distribs = [
            Normal("X", mu, sigma),
            Pareto("P", xm, alpha),
            ChiSquared("C", n),
            Exponential("E", sigma),
            # LogNormal("L", mu, sigma),
    ]
    for X in distribs:
        compdiff = cdf(X)(x) - simplify(X.pspace.density.compute_cdf()(x))
        compdiff = simplify(compdiff.rewrite(erfc))
        assert compdiff == 0

