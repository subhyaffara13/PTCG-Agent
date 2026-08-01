
def test_match_issue_21942():
    a, r, w = symbols('a, r, w', nonnegative=True)
    p = symbols('p', positive=True)
    g_ = Wild('g')
    pattern = g_ ** (1 / (1 - p))
    eq = (a * r ** (1 - p) + w ** (1 - p) * (1 - a)) ** (1 / (1 - p))
    m = {g_: a * r ** (1 - p) + w ** (1 - p) * (1 - a)}
    assert pattern.matches(eq) == m
    assert (-pattern).matches(-eq) == m
    assert pattern.matches(signsimp(eq)) is None

