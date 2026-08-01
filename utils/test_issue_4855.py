
def test_issue_4855():
    assert 1/O(1) != O(1)
    assert 1/O(x) != O(1/x)
    assert 1/O(x, (x, oo)) != O(1/x, (x, oo))

    f = Function('f')
    assert 1/O(f(x)) != O(1/x)

