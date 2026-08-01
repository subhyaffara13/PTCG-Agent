
def test_mean_skipna(values, dtype, result_dtype, skipna):
    # GH#15675
    df = DataFrame(
        {
            "val": values,
            "cat": ["A", "B"] * 5,
        }
    ).astype({"val": dtype})
    # We need to recast the expected values to the result_dtype because
    # Series.mean() changes the dtype to float64/object depending on the input dtype
    expected = (
        df.groupby("cat")["val"]
        .apply(lambda x: x.mean(skipna=skipna))
        .astype(result_dtype)
    )
    result = df.groupby("cat")["val"].mean(skipna=skipna)
    tm.assert_series_equal(result, expected)

