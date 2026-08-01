
def test_x_is_base_detection():
    eq = (x**2)**Rational(2, 3)
    assert eq.series() == x**Rational(4, 3)

