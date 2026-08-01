
def test_limits_simple_4aa():
    assert limit(x*(sqrt(x**2 + 1) - x), x, oo) == Rational(1)/2  # 214

