
def test_frame_single_columns_object_sum_axis_1():
    # GH 13758
    data = {
        "One": Series(["A", 1.2, np.nan]),
    }
    df = DataFrame(data)
    result = df.sum(axis=1)
    expected = Series(["A", 1.2, 0])
    tm.assert_series_equal(result, expected)

