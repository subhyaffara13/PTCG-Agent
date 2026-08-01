
def test_axis_columns_ignore_index():
    # GH 56478
    df = DataFrame([[1, 2]], columns=["d", "c"])
    result = df.sort_index(axis="columns", ignore_index=True)
    expected = DataFrame([[2, 1]])
    tm.assert_frame_equal(result, expected)

