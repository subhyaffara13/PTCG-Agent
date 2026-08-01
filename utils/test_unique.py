
def test_unique():
    assert tuple(unique((1, 2, 3))) == (1, 2, 3)
    assert tuple(unique((1, 2, 1, 3))) == (1, 2, 3)
    assert tuple(unique((1, 2, 3), key=iseven)) == (1, 2)


def test_unique(index_or_series_obj):
    obj = index_or_series_obj
    obj = np.repeat(obj, range(1, len(obj) + 1))
    result = obj.unique()

    # dict.fromkeys preserves the order
    unique_values = list(dict.fromkeys(obj.values))
    if isinstance(obj, pd.MultiIndex):
        expected = pd.MultiIndex.from_tuples(unique_values)
        expected.names = obj.names
        tm.assert_index_equal(result, expected, exact=True)
    elif isinstance(obj, pd.Index):
        expected = pd.Index(unique_values, dtype=obj.dtype)
        if isinstance(obj.dtype, pd.DatetimeTZDtype):
            expected = expected.normalize()
        tm.assert_index_equal(result, expected, exact=True)
    else:
        expected = np.array(unique_values)
        tm.assert_numpy_array_equal(result, expected)


def test_unique(names):
    mi = MultiIndex.from_arrays([[1, 2, 1, 2], [1, 1, 1, 2]], names=names)

    res = mi.unique()
    exp = MultiIndex.from_arrays([[1, 2, 2], [1, 1, 2]], names=mi.names)
    tm.assert_index_equal(res, exp)

    mi = MultiIndex.from_arrays([list("aaaa"), list("abab")], names=names)
    res = mi.unique()
    exp = MultiIndex.from_arrays([list("aa"), list("ab")], names=mi.names)
    tm.assert_index_equal(res, exp)

    mi = MultiIndex.from_arrays([list("aaaa"), list("aaaa")], names=names)
    res = mi.unique()
    exp = MultiIndex.from_arrays([["a"], ["a"]], names=mi.names)
    tm.assert_index_equal(res, exp)

    # GH #20568 - empty MI
    mi = MultiIndex.from_arrays([[], []], names=names)
    res = mi.unique()
    tm.assert_index_equal(mi, res)


def test_unique(tz_naive_fixture):
    idx = DatetimeIndex(["2017"] * 2, tz=tz_naive_fixture)
    expected = idx[:1]

    result = idx.unique()
    tm.assert_index_equal(result, expected)
    # GH#21737
    # Ensure the underlying data is consistent
    assert result[0] == expected[0]

