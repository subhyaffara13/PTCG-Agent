
def test_conjugate_priors():
    mu = Normal('mu', 2, 3)
    x = Normal('x', mu, 1)
    assert isinstance(simplify(density(mu, Eq(x, y), evaluate=False)(z)),
            Mul)

