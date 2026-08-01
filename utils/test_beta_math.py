
def test_beta_math():
    f = beta(x, y)
    F = lambdify((x, y), f, modules='math')

    assert abs(beta(1.3, 2.3) - F(1.3, 2.3)) <= 1e-10

