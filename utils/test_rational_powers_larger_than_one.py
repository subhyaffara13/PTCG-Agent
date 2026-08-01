
def test_rational_powers_larger_than_one():
    assert Rational(2, 3)**Rational(3, 2) == 2*sqrt(6)/9
    assert Rational(1, 6)**Rational(9, 4) == 6**Rational(3, 4)/216
    assert Rational(3, 7)**Rational(7, 3) == 9*3**Rational(1, 3)*7**Rational(2, 3)/343

