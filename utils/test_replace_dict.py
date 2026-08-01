
def test_replace_dict(any_string_dtype):
    # GH 51914
    series = Series(data=["A", "B", "C"], name="my_messy_col")
    new_series = series.str.replace(pat={"A": "a", "B": "b"})
    expected = Series(data=["a", "b", "C"], name="my_messy_col")
    tm.assert_series_equal(new_series, expected)

