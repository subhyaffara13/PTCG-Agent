
def test_groupby_resample_empty_sum_string(
    string_dtype_no_object, test_frame, min_count
):
    # https://github.com/pandas-dev/pandas/issues/60229
    dtype = string_dtype_no_object
    test_frame = test_frame.assign(B=pd.array([pd.NA] * len(test_frame), dtype=dtype))
    gbrs = test_frame.groupby("A").resample("40s")
    result = gbrs.sum(min_count=min_count)

    index = pd.MultiIndex(
        levels=[[1, 2, 3], [pd.to_datetime("2000-01-01", unit="ns").as_unit("ns")]],
        codes=[[0, 1, 2], [0, 0, 0]],
        names=["A", None],
    )
    value = "" if min_count == 0 else pd.NA
    expected = DataFrame({"B": value}, index=index, dtype=dtype)
    tm.assert_frame_equal(result, expected)

