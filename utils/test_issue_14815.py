
def test_issue_14815():
    x = Symbol('x', real=True)
    assert sqrt(x).is_extended_negative is False
    x = Symbol('x', real=False)
    assert sqrt(x).is_extended_negative is None
    x = Symbol('x', complex=True)
    assert sqrt(x).is_extended_negative is False
    x = Symbol('x', extended_real=True)
    assert sqrt(x).is_extended_negative is False
    assert sqrt(zoo, evaluate=False).is_extended_negative is False
    assert sqrt(nan, evaluate=False).is_extended_negative is None

