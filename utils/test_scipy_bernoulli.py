
def test_scipy_bernoulli():
    if not scipy:
        skip("scipy not installed")

    bern = lambdify((x,), bernoulli(x), modules='scipy')
    assert bern(1) == 0.5

