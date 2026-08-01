
def test_reset_index_interval_columns_object_cast():
    # GH 19136
    df = DataFrame(
        np.eye(2), index=Index([1, 2], name="Year"), columns=cut([1, 2], [0, 1, 2])
    )
    result = df.reset_index()
    expected = DataFrame(
        [[1, 1.0, 0.0], [2, 0.0, 1.0]],
        columns=Index(["Year", Interval(0, 1), Interval(1, 2)]),
    )
    tm.assert_frame_equal(result, expected)

