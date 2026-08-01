
def test_scipy_harmonic():
    if not scipy:
        skip("scipy not installed")

    hn = lambdify((x,), harmonic(x), modules='scipy')
    assert hn(2) == 1.5
    hnm = lambdify((x, y), harmonic(x, y), modules='scipy')
    assert hnm(2, 2) == 1.25

