
def test_take():
    assert list(take(2)([1, 2, 3])) == [1, 2]


def test_take():
    assert list(take(3, 'ABCDE')) == list('ABC')
    assert list(take(2, (3, 2, 1))) == list((3, 2))


def test_take():
    X = numbered_symbols()

    assert take(X, 5) == list(symbols('x0:5'))
    assert take(X, 5) == list(symbols('x5:10'))

    assert take([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]


def test_take(obj):
    # Check that no copy is made when we take all rows in original order
    obj_orig = obj.copy()
    obj2 = obj.take([0, 1])
    assert np.shares_memory(obj2.values, obj.values)

    obj2.iloc[0] = 0
    assert not np.shares_memory(obj2.values, obj.values)
    tm.assert_equal(obj, obj_orig)


def test_take():
    ser = Series([-1, 5, 6, 2, 4])

    actual = ser.take([1, 3, 4])
    expected = Series([5, 2, 4], index=[1, 3, 4])
    tm.assert_series_equal(actual, expected)

    actual = ser.take([-1, 3, 4])
    expected = Series([4, 2, 4], index=[4, 3, 4])
    tm.assert_series_equal(actual, expected)

    msg = "indices are out-of-bounds"
    with pytest.raises(IndexError, match=msg):
        ser.take([1, 10])
    with pytest.raises(IndexError, match=msg):
        ser.take([2, 5])


def test_take(idx):
    indexer = [4, 3, 0, 2]
    result = idx.take(indexer)
    expected = idx[indexer]
    assert result.equals(expected)

    # GH 10791
    msg = "'MultiIndex' object has no attribute 'freq'"
    with pytest.raises(AttributeError, match=msg):
        idx.freq


def test_take(string_list):
    sarr = np.array(string_list, dtype="T")
    res = sarr.take(np.arange(len(string_list)))
    assert_array_equal(sarr, res)

    # make sure it also works for out
    out = np.empty(len(string_list), dtype="T")
    out[0] = "hello"
    res = sarr.take(np.arange(len(string_list)), out=out)
    assert res is out
    assert_array_equal(sarr, res)

