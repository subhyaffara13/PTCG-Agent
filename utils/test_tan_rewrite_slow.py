
def test_tan_rewrite_slow():
    assert 0 == (cos(pi/34)*tan(pi/34) - sin(pi/34)).rewrite(pow)
    assert 0 == (cos(pi/17)*tan(pi/17) - sin(pi/17)).rewrite(pow)
    assert tan(pi/19).rewrite(pow) == tan(pi/19)
    assert tan(pi*Rational(8, 19)).rewrite(sqrt) == tan(pi*Rational(8, 19))
    assert tan(pi*Rational(2, 5), evaluate=False).rewrite(sqrt) == sqrt(sqrt(5)/8 +
               Rational(5, 8))/(Rational(-1, 4) + sqrt(5)/4)

