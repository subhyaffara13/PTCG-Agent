
def test_cut_unordered_with_series_labels():
    # https://github.com/pandas-dev/pandas/issues/36603
    ser = Series([1, 2, 3, 4, 5])
    bins = Series([0, 2, 4, 6])
    labels = Series(["a", "b", "c"])
    result = cut(ser, bins=bins, labels=labels, ordered=False)
    expected = Series(["a", "a", "b", "b", "c"], dtype="category")
    tm.assert_series_equal(result, expected)

