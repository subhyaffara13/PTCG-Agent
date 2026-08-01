
def test_issue_3538():
    v = sympify("exp(x)")
    assert v == exp(x)
    assert type(v) == type(exp(x))
    assert str(type(v)) == str(type(exp(x)))

