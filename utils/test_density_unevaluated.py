
def test_density_unevaluated():
    X = Normal('X', 0, 1)
    Y = Normal('Y', 0, 2)
    assert isinstance(density(X+Y, evaluate=False)(z), Integral)

