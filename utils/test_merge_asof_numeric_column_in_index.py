
def test_merge_asof_numeric_column_in_index():
    # GH#34488
    left = pd.DataFrame({"b": [10, 11, 12]}, index=Index([1, 2, 3], name="a"))
    right = pd.DataFrame({"c": [20, 21, 22]}, index=Index([0, 2, 3], name="a"))

    result = merge_asof(left, right, left_on="a", right_on="a")
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [10, 11, 12], "c": [20, 21, 22]})
    tm.assert_frame_equal(result, expected)

