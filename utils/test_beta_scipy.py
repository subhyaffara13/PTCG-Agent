
def test_beta_scipy():
    if not scipy:
        skip("scipy not installed")

    f = beta(x, y)
    F = lambdify((x, y), f, modules='scipy')

    assert abs(beta(1.3, 2.3) - F(1.3, 2.3)) <= 1e-10

