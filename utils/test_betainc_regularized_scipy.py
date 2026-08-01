
def test_betainc_regularized_scipy():
    if not scipy:
        skip("scipy not installed")

    f = betainc_regularized(w, x, y, z)
    F = lambdify((w, x, y, z), f, modules='scipy')

    assert abs(betainc_regularized(0.2, 3.5, 0.1, 1) - F(0.2, 3.5, 0.1, 1)) <= 1e-10

