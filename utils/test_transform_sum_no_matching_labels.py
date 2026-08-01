
def test_transform_sum_no_matching_labels():
    df = DataFrame({"X": [1.0, -93204, 4935]})
    series = Series(["A", "B", "C"])

    result = df.groupby(series, as_index=False).transform("sum")
    expected = DataFrame({"X": [1.0, -93204, 4935]})
    tm.assert_frame_equal(result, expected)

