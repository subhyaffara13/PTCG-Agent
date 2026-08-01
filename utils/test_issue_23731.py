
def test_issue_23731():
    i = symbols('i', integer=True)
    assert unchanged(Eq, i, 1.0)
    assert unchanged(Eq, i/2, 0.5)
    ni = symbols('ni', integer=False)
    assert Eq(ni, 1) == False
    assert unchanged(Eq, ni, .1)
    assert Eq(ni, 1.0) == False
    nr = symbols('nr', rational=False)
    assert Eq(nr, .1) == False

