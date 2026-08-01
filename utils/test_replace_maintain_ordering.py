
def test_replace_maintain_ordering():
    # GH51016
    dtype = pd.CategoricalDtype([0, 1, 2], ordered=True)
    ser = pd.Series([0, 1, 2], dtype=dtype)
    result = ser.replace(0, 2)
    expected = pd.Series([2, 1, 2], dtype=dtype)
    tm.assert_series_equal(expected, result, check_category_order=True)

