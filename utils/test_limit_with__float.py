
def test_limit_with_Float():
    k = symbols("k")
    assert limit(1.0 ** k, k, oo) == 1
    assert limit(0.3*1.0**k, k, oo) == Rational(3, 10)

