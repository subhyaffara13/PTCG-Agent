
def test_unflatten():
    r = list(range(10))
    assert unflatten(r) == list(zip(r[::2], r[1::2]))
    assert unflatten(r, 5) == [tuple(r[:5]), tuple(r[5:])]
    raises(ValueError, lambda: unflatten(list(range(10)), 3))
    raises(ValueError, lambda: unflatten(list(range(10)), -2))

