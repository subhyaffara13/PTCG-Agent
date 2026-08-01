
def test_concat_series():
    ser = Series([1, 2], name="a")
    ser2 = Series([3, 4], name="b")
    ser_orig = ser.copy()
    ser2_orig = ser2.copy()
    result = concat([ser, ser2], axis=1)

    assert np.shares_memory(get_array(result, "a"), ser.values)
    assert np.shares_memory(get_array(result, "b"), ser2.values)

    result.iloc[0, 0] = 100
    assert not np.shares_memory(get_array(result, "a"), ser.values)
    assert np.shares_memory(get_array(result, "b"), ser2.values)

    result.iloc[0, 1] = 1000
    assert not np.shares_memory(get_array(result, "b"), ser2.values)
    tm.assert_series_equal(ser, ser_orig)
    tm.assert_series_equal(ser2, ser2_orig)


def test_concat_series(to_concat_dtypes, result_dtype):
    result = pd.concat([pd.Series([1, 2, pd.NA], dtype=t) for t in to_concat_dtypes])
    expected = pd.concat([pd.Series([1, 2, pd.NA], dtype=object)] * 2).astype(
        result_dtype
    )
    tm.assert_series_equal(result, expected)


def test_concat_series(to_concat_dtypes, result_dtype):
    # we expect the same dtypes as we would get with non-masked inputs,
    #  just masked where available.

    result = pd.concat([pd.Series([0, 1, pd.NA], dtype=t) for t in to_concat_dtypes])
    expected = pd.concat([pd.Series([0, 1, pd.NA], dtype=object)] * 2).astype(
        result_dtype
    )
    tm.assert_series_equal(result, expected)

    # order doesn't matter for result
    result = pd.concat(
        [pd.Series([0, 1, pd.NA], dtype=t) for t in to_concat_dtypes[::-1]]
    )
    expected = pd.concat([pd.Series([0, 1, pd.NA], dtype=object)] * 2).astype(
        result_dtype
    )
    tm.assert_series_equal(result, expected)


def test_concat_series(request, to_concat_dtypes, result_dtype):
    if any(storage == "pyarrow" for storage, _ in to_concat_dtypes) and not HAS_PYARROW:
        pytest.skip("Could not import 'pyarrow'")

    ser_list = [
        pd.Series(["a", "b", None], dtype=pd.StringDtype(storage, na_value))
        for storage, na_value in to_concat_dtypes
    ]

    result = pd.concat(ser_list, ignore_index=True)
    expected = pd.Series(
        ["a", "b", None, "a", "b", None], dtype=pd.StringDtype(*result_dtype)
    )
    tm.assert_series_equal(result, expected)

    # order doesn't matter for result
    result = pd.concat(ser_list[::1], ignore_index=True)
    tm.assert_series_equal(result, expected)

