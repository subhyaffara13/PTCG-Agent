
def test_issue_9351():
    assert exp(x).series(x, 10, 1) == exp(10) + Order(x - 10, (x, 10))

