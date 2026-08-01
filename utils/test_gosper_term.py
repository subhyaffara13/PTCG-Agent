
def test_gosper_term():
    assert gosper_term((4*k + 1)*factorial(
        k)/factorial(2*k + 1), k) == (-k - S.Half)/(k + Rational(1, 4))

