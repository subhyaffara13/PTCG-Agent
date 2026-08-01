
def test_join_cross(input_col, output_cols):
    # GH#5401
    left = DataFrame({"a": [1, 3]})
    right = DataFrame({input_col: [3, 4]})
    result = left.join(right, how="cross", lsuffix="_x", rsuffix="_y")
    expected = DataFrame({output_cols[0]: [1, 1, 3, 3], output_cols[1]: [3, 4, 3, 4]})
    tm.assert_frame_equal(result, expected)

