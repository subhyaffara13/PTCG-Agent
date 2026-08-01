
def test_issue_15920():
    r = rootof(x**5 - x + 1, 0)
    p = Integral(x, (x, 1, y))
    assert unchanged(Eq, r, p)

