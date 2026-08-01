
def test_multifunc_skipna(func, values, dtype, result_dtype, skipna):
    # GH#15675
    df = DataFrame(
        {
            "val": values,
            "cat": ["A", "B"] * 5,
        }
    ).astype({"val": dtype})
    # We need to recast the expected values to the result_dtype as some operations
    # change the dtype
    expected = (
        df.groupby("cat")["val"]
        .apply(lambda x: getattr(x, func)(skipna=skipna))
        .astype(result_dtype)
    )
    result = getattr(df.groupby("cat")["val"], func)(skipna=skipna)
    tm.assert_series_equal(result, expected)

