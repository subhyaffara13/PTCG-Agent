
def test_omgissue_203():
    h = hyper((-5, -3, -4), (-6, -6), 1)
    assert hyperexpand(h) == Rational(1, 30)
    h = hyper((-6, -7, -5), (-6, -6), 1)
    assert hyperexpand(h) == Rational(-1, 6)

