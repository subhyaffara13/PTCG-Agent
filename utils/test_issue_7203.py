
def test_issue_7203():
    assert series(cos(x), x, pi, 3) == \
        -1 + (x - pi)**2/2 + O((x - pi)**3, (x, pi))

