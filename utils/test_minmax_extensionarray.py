
def test_minmax_extensionarray(method, numeric_only):
    # https://github.com/pandas-dev/pandas/issues/32651
    int64_info = np.iinfo("int64")
    ser = Series([int64_info.max, None, int64_info.min], dtype=pd.Int64Dtype())
    df = DataFrame({"Int64": ser})
    result = getattr(df, method)(numeric_only=numeric_only)
    expected = Series(
        [getattr(int64_info, method)],
        dtype="Int64",
        index=Index(["Int64"]),
    )
    tm.assert_series_equal(result, expected)

