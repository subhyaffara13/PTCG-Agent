
def test_issue_18762():
    e, p = symbols('e p')
    g0 = sqrt(1 + e**2 - 2*e*cos(p))
    assert len(g0.series(e, 1, 3).args) == 4

