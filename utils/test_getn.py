
def test_getn():
    # other lines are tested incidentally by the suite
    assert O(x).getn() == 1
    assert O(x/log(x)).getn() == 1
    assert O(x**2/log(x)**2).getn() == 2
    assert O(x*log(x)).getn() == 1
    raises(NotImplementedError, lambda: (O(x) + O(y)).getn())

