
def test_Sum_dummy_eq():
    assert not Sum(x, (x, a, b)).dummy_eq(1)
    assert not Sum(x, (x, a, b)).dummy_eq(Sum(x, (x, a, b), (a, 1, 2)))
    assert not Sum(x, (x, a, b)).dummy_eq(Sum(x, (x, a, c)))
    assert Sum(x, (x, a, b)).dummy_eq(Sum(x, (x, a, b)))
    d = Dummy()
    assert Sum(x, (x, a, d)).dummy_eq(Sum(x, (x, a, c)), c)
    assert not Sum(x, (x, a, d)).dummy_eq(Sum(x, (x, a, c)))
    assert Sum(x, (x, a, c)).dummy_eq(Sum(y, (y, a, c)))
    assert Sum(x, (x, a, d)).dummy_eq(Sum(y, (y, a, c)), c)
    assert not Sum(x, (x, a, d)).dummy_eq(Sum(y, (y, a, c)))

