
def test_issue_15751():
    f = y(n) + 21*y(n + 1) - 273*y(n + 2) - 1092*y(n + 3) + 1820*y(n + 4) + 1092*y(n + 5) - 273*y(n + 6) - 21*y(n + 7) + y(n + 8)
    assert rsolve(f, y(n)) is not None

