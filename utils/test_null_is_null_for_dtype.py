
def test_null_is_null_for_dtype(
    sort, dtype, nulls_fixture, nulls_fixture2, test_series
):
    # GH#48506 - groups should always result in using the null for the dtype
    df = pd.DataFrame({"a": [1, 2]})
    groups = pd.Series([nulls_fixture, nulls_fixture2], dtype=dtype)
    obj = df["a"] if test_series else df
    gb = obj.groupby(groups, dropna=False, sort=sort)
    result = gb.sum()
    index = pd.Index([na_value_for_dtype(groups.dtype)])
    expected = pd.DataFrame({"a": [3]}, index=index)
    if test_series:
        tm.assert_series_equal(result, expected["a"])
    else:
        tm.assert_frame_equal(result, expected)

