
def test_map_categorical_with_nan_values(data, expected_dtype):
    # GH 20714 bug fixed in: GH 24275
    def func(val):
        return val.split("-")[0]

    s = Series(data, dtype="category")

    result = s.map(func, na_action="ignore")
    expected = Series(["1", "1", np.nan], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

