
def test_issue_17421():
    assert N(acos(-I + acosh(cosh(cosh(1) + I)))) == 1.0*I

