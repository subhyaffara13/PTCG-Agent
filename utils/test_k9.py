
def test_K9():
    z = symbols('z', positive=True)
    assert simplify(sqrt(1/z) - 1/sqrt(z)) == 0

