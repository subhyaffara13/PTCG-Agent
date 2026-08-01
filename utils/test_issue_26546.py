
def test_issue_26546():
    x = Symbol('x', real=True)
    assert x.is_extended_real is True
    assert sqrt(x+I).is_extended_real is False
    assert Pow(x+I, S.Half).is_extended_real is False
    assert Pow(x+I, Rational(1,2)).is_extended_real is False
    assert Pow(x+I, Rational(1,13)).is_extended_real is False
    assert Pow(x+I, Rational(2,3)).is_extended_real is None

