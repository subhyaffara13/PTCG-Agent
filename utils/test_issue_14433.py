
def test_issue_14433():
    assert (Rational(2, 3)*x in QQ.frac_field(1/x)) is True
    assert (1/x in QQ.frac_field(x)) is True
    assert ((x**2 + y**2) in QQ.frac_field(1/x, 1/y)) is True
    assert ((x + y) in QQ.frac_field(1/x, y)) is True
    assert ((x - y) in QQ.frac_field(x, 1/y)) is True

