
def test_ufunc_reduce_raises(values):
    arr = pd.array(values, dtype="boolean")

    res = np.add.reduce(arr)
    if arr[-1] is pd.NA:
        expected = pd.NA
    else:
        expected = arr._data.sum()
    tm.assert_almost_equal(res, expected)


def test_ufunc_reduce_raises(values):
    arr = pd.array(values, dtype="Float64")

    res = np.add.reduce(arr)
    expected = arr.sum(skipna=False)
    tm.assert_almost_equal(res, expected)


def test_ufunc_reduce_raises(values):
    arr = pd.array(values)

    res = np.add.reduce(arr)
    expected = arr.sum(skipna=False)
    tm.assert_almost_equal(res, expected)

