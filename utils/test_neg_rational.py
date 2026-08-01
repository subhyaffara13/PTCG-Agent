
def test_neg_rational():
    r = Rational(-3, 4)
    assert r.is_positive is False
    assert r.is_nonpositive is True
    assert r.is_negative is True
    assert r.is_nonnegative is False
    r = Rational(-1, 4)
    assert r.is_nonpositive is True
    assert r.is_positive is False
    assert r.is_negative is True
    assert r.is_nonnegative is False
    r = Rational(-5, 4)
    assert r.is_negative is True
    assert r.is_positive is False
    assert r.is_nonpositive is True
    assert r.is_nonnegative is False
    r = Rational(-5, 3)
    assert r.is_nonnegative is False
    assert r.is_positive is False
    assert r.is_negative is True
    assert r.is_nonpositive is True

