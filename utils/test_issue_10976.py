
def test_issue_10976():
    s, x = symbols('s x', real=True)
    assert limit(erf(s*x)/erf(s), s, 0) == x

