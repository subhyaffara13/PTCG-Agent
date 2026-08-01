
def test_groupby_op_with_nullables(na_option):
    # GH 54206
    df = DataFrame({"x": [None]}, dtype="Float64")
    result = df.groupby("x", dropna=False)["x"].rank(method="min", na_option=na_option)
    expected = Series([1.0], dtype="Float64", name=result.name)
    tm.assert_series_equal(result, expected)

