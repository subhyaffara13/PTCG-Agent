
def test_apply_with_duplicated_non_sorted_axis(test_series):
    # GH 30667
    df = DataFrame(
        [["x", "p"], ["x", "p"], ["x", "o"]], columns=["X", "Y"], index=[1, 2, 2]
    )
    if test_series:
        ser = df.set_index("Y")["X"]
        result = ser.groupby(level=0, group_keys=False).apply(lambda x: x)
        expected = ser
        tm.assert_series_equal(result, expected)
    else:
        result = df.groupby("Y", group_keys=False).apply(lambda x: x)
        expected = df[["X"]]
        tm.assert_frame_equal(result, expected)

