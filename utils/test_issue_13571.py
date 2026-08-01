
def test_issue_13571():
    assert limit(uppergamma(x, 1) / gamma(x), x, oo) == 1

