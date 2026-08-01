
def test_getO():
    assert (x).getO() is None
    assert (x).removeO() == x
    assert (O(x)).getO() == O(x)
    assert (O(x)).removeO() == 0
    assert (z + O(x) + O(y)).getO() == O(x) + O(y)
    assert (z + O(x) + O(y)).removeO() == z
    raises(NotImplementedError, lambda: (O(x) + O(y)).getn())

