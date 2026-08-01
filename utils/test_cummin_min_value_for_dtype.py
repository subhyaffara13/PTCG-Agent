
def test_cummin_min_value_for_dtype(dtypes_for_minmax):
    dtype = dtypes_for_minmax[0]
    min_val = dtypes_for_minmax[1]

    # GH 15048
    base_df = DataFrame({"A": [1, 1, 1, 1, 2, 2, 2, 2], "B": [3, 4, 3, 2, 2, 3, 2, 1]})
    expected_mins = [3, 3, 3, 2, 2, 2, 2, 1]
    expected = DataFrame({"B": expected_mins}).astype(dtype)
    df = base_df.astype(dtype)
    df.loc[[2, 6], "B"] = min_val
    df.loc[[1, 5], "B"] = min_val + 1
    expected.loc[[2, 3, 6, 7], "B"] = min_val
    expected.loc[[1, 5], "B"] = min_val + 1  # should not be rounded to min_val
    result = df.groupby("A").cummin()
    tm.assert_frame_equal(result, expected, check_exact=True)
    expected = (
        df.groupby("A", group_keys=False).B.apply(lambda x: x.cummin()).to_frame()
    )
    tm.assert_frame_equal(result, expected, check_exact=True)

