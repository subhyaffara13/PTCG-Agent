
def test_transform_sum_one_column_with_matching_labels_and_missing_labels():
    df = DataFrame({"X": [1.0, -93204, 4935]})
    series = Series(["A", "A"])

    result = df.groupby(series, as_index=False).transform("sum")
    expected = DataFrame({"X": [-93203.0, -93203.0, np.nan]})
    tm.assert_frame_equal(result, expected)

