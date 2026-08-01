
def test_mean_nullable_int_axis_1():
    # GH##36585
    df = DataFrame(
        {"a": [1, 2, 3, 4], "b": Series([1, 2, 4, None], dtype=pd.Int64Dtype())}
    )

    result = df.mean(axis=1, skipna=True)
    expected = Series([1.0, 2.0, 3.5, 4.0], dtype="Float64")
    tm.assert_series_equal(result, expected)

    result = df.mean(axis=1, skipna=False)
    expected = Series([1.0, 2.0, 3.5, pd.NA], dtype="Float64")
    tm.assert_series_equal(result, expected)

