
def test_replace_from_index():
    # https://github.com/pandas-dev/pandas/issues/61622
    idx = pd.Index(["a", "b", "c"], dtype="string[pyarrow]")
    expected = pd.Series(["d", "b", "c"], dtype="string[pyarrow]")
    result = pd.Series(idx).replace({"z": "b", "a": "d"})
    tm.assert_series_equal(result, expected)

