
def test_transform_sum_one_column_no_matching_labels():
    df = DataFrame({"X": [1.0]})
    series = Series(["Y"])
    result = df.groupby(series, as_index=False).transform("sum")
    expected = DataFrame({"X": [1.0]})
    tm.assert_frame_equal(result, expected)

