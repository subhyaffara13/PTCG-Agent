
def test_decompose_power():
    assert decompose_power(x) == (x, 1)
    assert decompose_power(x**2) == (x, 2)
    assert decompose_power(x**(2*y)) == (x**y, 2)
    assert decompose_power(x**(2*y/3)) == (x**(y/3), 2)
    assert decompose_power(x**(y*Rational(2, 3))) == (x**(y/3), 2)

