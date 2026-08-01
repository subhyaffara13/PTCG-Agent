
def test_series_add_sub_with_UInt64():
    # GH 22023
    series1 = Series([1, 2, 3])
    series2 = Series([2, 1, 3], dtype="UInt64")

    result = series1 + series2
    expected = Series([3, 3, 6], dtype="Float64")
    tm.assert_series_equal(result, expected)

    result = series1 - series2
    expected = Series([-1, 1, 0], dtype="Float64")
    tm.assert_series_equal(result, expected)

