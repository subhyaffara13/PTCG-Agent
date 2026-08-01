
def test_replace_categorical_series(to_replace, value, expected):
    # GH 31720
    ser = pd.Series([1, 2, 3], dtype="category")
    result = ser.replace(to_replace, value)
    expected = pd.Series(Categorical(expected, categories=[1, 2, 3]))
    tm.assert_series_equal(result, expected)

