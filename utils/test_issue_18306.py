
def test_issue_18306():
    assert limit(sin(sqrt(x))/sqrt(sin(x)), x, 0, '+') == 1

