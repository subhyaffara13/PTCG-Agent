
def test_issue_11884():
    assert cos(x).series(x, 1, n=1) == cos(1) + O(x - 1, (x, 1))

