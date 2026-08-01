
def test_issue_18969():
    a, b = symbols('a b', positive=True)
    assert limit(LambertW(a), a, b) == LambertW(b)
    assert limit(exp(LambertW(a)), a, b) == exp(LambertW(b))

