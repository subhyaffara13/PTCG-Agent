
def test_issue_16536():
    if not scipy:
        skip("scipy not installed")

    a = symbols('a')
    f1 = lowergamma(a, x)
    F = lambdify((a, x), f1, modules='scipy')
    assert abs(lowergamma(1, 3) - F(1, 3)) <= 1e-10

    f2 = uppergamma(a, x)
    F = lambdify((a, x), f2, modules='scipy')
    assert abs(uppergamma(1, 3) - F(1, 3)) <= 1e-10

