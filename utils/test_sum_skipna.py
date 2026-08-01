
def test_sum_skipna(values, dtype, skipna):
    # GH#15675
    df = DataFrame(
        {
            "val": values,
            "cat": ["A", "B"] * 5,
        }
    ).astype({"val": dtype})
    # We need to recast the expected values to the original dtype because
    # Series.sum() changes the dtype
    expected = (
        df.groupby("cat")["val"].apply(lambda x: x.sum(skipna=skipna)).astype(dtype)
    )
    result = df.groupby("cat")["val"].sum(skipna=skipna)
    tm.assert_series_equal(result, expected)

