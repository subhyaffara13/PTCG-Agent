
def test_isin():
    values = [("foo", 2), ("bar", 3), ("quux", 4)]

    idx = MultiIndex.from_arrays([["qux", "baz", "foo", "bar"], np.arange(4)])
    result = idx.isin(values)
    expected = np.array([False, False, True, True])
    tm.assert_numpy_array_equal(result, expected)

    # empty, return dtype bool
    idx = MultiIndex.from_arrays([[], []])
    result = idx.isin(values)
    assert len(result) == 0
    assert result.dtype == np.bool_


def test_isin(dtype, fixed_now_ts):
    s = pd.Series(["a", "b", None], dtype=dtype)

    result = s.isin(["a", "c"])
    expected = pd.Series([True, False, False])
    tm.assert_series_equal(result, expected)

    result = s.isin(["a", pd.NA])
    expected = pd.Series([True, False, True])
    tm.assert_series_equal(result, expected)

    result = s.isin([])
    expected = pd.Series([False, False, False])
    tm.assert_series_equal(result, expected)

    result = s.isin(["a", fixed_now_ts])
    expected = pd.Series([True, False, False])
    tm.assert_series_equal(result, expected)

    result = s.isin([fixed_now_ts])
    expected = pd.Series([False, False, False])
    tm.assert_series_equal(result, expected)

