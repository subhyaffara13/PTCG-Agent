
def test_simple_7():
    assert 1 + O(1) == O(1)
    assert 2 + O(1) == O(1)
    assert x + O(1) == O(1)
    assert 1/x + O(1) == 1/x + O(1)

