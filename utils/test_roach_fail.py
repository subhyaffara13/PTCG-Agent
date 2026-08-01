
def test_roach_fail():
    assert can_do([Rational(-1, 2), 1], [Rational(1, 4), S.Half, Rational(3, 4)])  # PFDD
    assert can_do([Rational(3, 2)], [Rational(5, 2), 5])  # struve function
    assert can_do([Rational(-1, 2), S.Half, 1], [Rational(3, 2), Rational(5, 2)])  # polylog, pfdd
    assert can_do([1, 2, 3], [S.Half, 4])  # XXX ?
    assert can_do([S.Half], [Rational(-1, 3), Rational(-1, 2), Rational(-2, 3)])  # PFDD ?

