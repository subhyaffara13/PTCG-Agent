
def test_issue_8433():
    d, t = symbols('d t', positive=True)
    assert limit(erf(1 - t/d), t, oo) == -1

