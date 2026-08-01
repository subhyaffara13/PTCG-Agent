
def test_issue_26856():
    raises(ValueError, lambda: (2**x).series(x, oo, -1))

