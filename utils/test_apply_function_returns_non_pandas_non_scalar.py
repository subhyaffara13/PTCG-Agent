
def test_apply_function_returns_non_pandas_non_scalar(function, expected_values):
    # GH 31441
    df = DataFrame(["A", "A", "B", "B"], columns=["groups"])
    result = df.groupby("groups").apply(function)
    expected = Series(expected_values, index=Index(["A", "B"], name="groups"))
    tm.assert_series_equal(result, expected)

