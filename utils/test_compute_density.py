
def test_compute_density():
    X = Normal('X', 0, Symbol("sigma")**2)
    raises(ValueError, lambda: density(X**5 + X))

