
def test_conversion1():
    a = list2numpy([x**2, x])
    #looks like an array?
    assert isinstance(a, ndarray)
    assert a[0] == x**2
    assert a[1] == x
    assert len(a) == 2

