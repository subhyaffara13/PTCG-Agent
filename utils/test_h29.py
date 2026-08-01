
def test_H29():
    assert factor(4*x**2 - 21*x*y + 20*y**2, modulus=3) == (x + y)*(x - y)

