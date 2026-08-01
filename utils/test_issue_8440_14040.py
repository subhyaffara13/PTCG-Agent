
def test_issue_8440_14040():
    assert integrate(1/x, (x, -1, 1)) is S.NaN
    assert integrate(1/(x + 1), (x, -2, 3)) is S.NaN

