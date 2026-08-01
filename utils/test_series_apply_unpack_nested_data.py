
def test_series_apply_unpack_nested_data():
    # GH#55189
    ser = Series([[1, 2, 3], [4, 5, 6, 7]])
    result = ser.apply(lambda x: Series(x))
    expected = DataFrame({0: [1.0, 4.0], 1: [2.0, 5.0], 2: [3.0, 6.0], 3: [np.nan, 7]})
    tm.assert_frame_equal(result, expected)

