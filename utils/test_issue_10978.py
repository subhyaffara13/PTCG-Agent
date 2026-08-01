
def test_issue_10978():
    assert LambertW(x).limit(x, 0) == 0

