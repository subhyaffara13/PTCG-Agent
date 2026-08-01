
def test_K8():
    z = symbols('z', complex=True)
    assert simplify(sqrt(1/z) - 1/sqrt(z)) != 0  # Passes
    z = symbols('z', complex=True, negative=False)
    assert simplify(sqrt(1/z) - 1/sqrt(z)) == 0  # Fails

