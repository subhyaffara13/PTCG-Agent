
def test_issue_10475():
    a = Symbol('a', extended_real=True)
    b = Symbol('b', extended_positive=True)
    s = Symbol('s', zero=False)

    assert zeta(2 + I).is_finite
    assert zeta(1).is_finite is False
    assert zeta(x).is_finite is None
    assert zeta(x + I).is_finite is None
    assert zeta(a).is_finite is None
    assert zeta(b).is_finite is None
    assert zeta(-b).is_finite is True
    assert zeta(b**2 - 2*b + 1).is_finite is None
    assert zeta(a + I).is_finite is True
    assert zeta(b + 1).is_finite is True
    assert zeta(s + 1).is_finite is True

