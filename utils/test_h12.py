
def test_H12():
    num = x**2 - 4
    den = x**2 + 4*x + 4
    assert simplify(num/den) == (x - 2)/(x + 2)

