
def test_logbug4():
    assert log(2 + O(x)).nseries(x, 0, 2) == log(2) + O(x, x)

