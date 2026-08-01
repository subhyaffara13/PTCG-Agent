
def test_transform_sum_one_column_with_matching_labels():
    df = DataFrame({"X": [1.0, -93204, 4935]})
    series = Series(["A", "B", "A"])

    result = df.groupby(series, as_index=False).transform("sum")
    expected = DataFrame({"X": [4936.0, -93204, 4936.0]})
    tm.assert_frame_equal(result, expected)

