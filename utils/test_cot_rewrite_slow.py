
def test_cot_rewrite_slow():
    assert cot(pi*Rational(4, 34)).rewrite(pow).ratsimp() == \
        (cos(pi*Rational(4, 34))/sin(pi*Rational(4, 34))).rewrite(pow).ratsimp()
    assert cot(pi*Rational(4, 17)).rewrite(pow) == \
        (cos(pi*Rational(4, 17))/sin(pi*Rational(4, 17))).rewrite(pow)
    assert cot(pi/19).rewrite(pow) == cot(pi/19)
    assert cot(pi/19).rewrite(sqrt) == cot(pi/19)
    assert cot(pi*Rational(2, 5), evaluate=False).rewrite(sqrt) == \
        (Rational(-1, 4) + sqrt(5)/4) / sqrt(sqrt(5)/8 + Rational(5, 8))

