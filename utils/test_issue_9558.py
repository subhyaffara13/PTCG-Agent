
def test_issue_9558():
    assert limit(sin(x)**15, x, 0, '-') == 0

