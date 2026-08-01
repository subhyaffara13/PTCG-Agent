
def test_H23():
    f = x**11 + x + 1
    g = (x**2 + x + 1) * (x**9 - x**8 + x**6 - x**5 + x**3 - x**2 + 1)
    assert factor(f, modulus=65537) == g

