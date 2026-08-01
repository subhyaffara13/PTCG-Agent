
def test_same():
    x = np.arange(10)
    y = np.arange(10)
    bx, by = broadcast_arrays(x, y)
    assert_array_equal(x, bx)
    assert_array_equal(y, by)


def test_same():
    equal = {"A": 2, "B": 2, "C": 2}
    slightly_different = {"A": 2, "B": 1, "C": 2}
    different = {"A": 2, "B": 8, "C": 18}
    assert _same(equal)
    assert not _same(slightly_different)
    assert _same(slightly_different, tol=1)
    assert not _same(different)
    assert not _same(different, tol=4)

