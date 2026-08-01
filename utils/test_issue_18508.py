
def test_issue_18508():
    assert limit(sin(x)/sqrt(1-cos(x)), x, 0) == sqrt(2)
    assert limit(sin(x)/sqrt(1-cos(x)), x, 0, dir='+') == sqrt(2)
    assert limit(sin(x)/sqrt(1-cos(x)), x, 0, dir='-') == -sqrt(2)

