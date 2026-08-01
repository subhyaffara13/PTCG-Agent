
def test_issue_11496():
    assert limit(erfc(log(1/x)), x, oo) == 2

