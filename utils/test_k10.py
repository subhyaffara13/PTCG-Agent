
def test_K10():
    z = symbols('z', negative=True)
    assert simplify(sqrt(1/z) + 1/sqrt(z)) == 0

