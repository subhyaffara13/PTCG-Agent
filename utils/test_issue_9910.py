
def test_issue_9910():
    assert O(x*log(x) + sin(x), (x, oo)) == O(x*log(x), (x, oo))

