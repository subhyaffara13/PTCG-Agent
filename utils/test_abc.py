
def test_abc():
    x = numbers.Float(5)
    assert(isinstance(x, nums.Number))
    assert(isinstance(x, numbers.Number))
    assert(isinstance(x, nums.Real))
    y = numbers.Rational(1, 3)
    assert(isinstance(y, nums.Number))
    assert(y.numerator == 1)
    assert(y.denominator == 3)
    assert(isinstance(y, nums.Rational))
    z = numbers.Integer(3)
    assert(isinstance(z, nums.Number))
    assert(isinstance(z, numbers.Number))
    assert(isinstance(z, nums.Rational))
    assert(isinstance(z, numbers.Rational))
    assert(isinstance(z, nums.Integral))

