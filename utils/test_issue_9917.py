
def test_issue_9917():
    assert O(x*sin(x) + 1, (x, oo)) == O(x, (x, oo))

