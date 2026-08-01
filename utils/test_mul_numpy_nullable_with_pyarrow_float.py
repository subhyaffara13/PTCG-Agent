
def test_mul_numpy_nullable_with_pyarrow_float():
    # GH#58602
    left = pd.Series(range(5), dtype="Float64")
    right = pd.Series(range(5), dtype="float64[pyarrow]")

    expected = pd.Series([0, 1, 4, 9, 16], dtype="float64[pyarrow]")

    result = left * right
    tm.assert_series_equal(result, expected)

    result2 = right * left
    tm.assert_series_equal(result2, expected)

    # while we're here, let's check __eq__
    result3 = left == right
    expected3 = pd.Series([True] * 5, dtype="bool[pyarrow]")
    tm.assert_series_equal(result3, expected3)

    result4 = right == left
    tm.assert_series_equal(result4, expected3)

