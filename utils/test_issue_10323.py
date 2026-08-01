
def test_issue_10323():
    assert ceiling(sqrt(2**30 + 1)) == 2**15 + 1

