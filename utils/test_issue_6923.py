
def test_issue_6923():
    assert (-2*x*sqrt(2)).subs(2*x, y) == -sqrt(2)*y

