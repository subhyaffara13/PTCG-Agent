
def test_issue_16222():
    assert limit(exp(x), x, 1000000000) == exp(1000000000)

