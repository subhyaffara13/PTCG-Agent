
def test_roach():
    # Kelly B. Roach.  Meijer G Function Representations.
    # Section "Gallery"
    assert can_do([S.Half], [Rational(9, 2)])
    assert can_do([], [1, Rational(5, 2), 4])
    assert can_do([Rational(-1, 2), 1, 2], [3, 4])
    assert can_do([Rational(1, 3)], [Rational(-2, 3), Rational(-1, 2), S.Half, 1])
    assert can_do([Rational(-3, 2), Rational(-1, 2)], [Rational(-5, 2), 1])
    assert can_do([Rational(-3, 2), ], [Rational(-1, 2), S.Half])  # shine-integral
    assert can_do([Rational(-3, 2), Rational(-1, 2)], [2])  # elliptic integrals

