
def test_cut_with_duplicated_index_lowest_included():
    # GH 42185
    expected = Series(
        [Interval(-0.001, 2, closed="right")] * 3
        + [Interval(2, 4, closed="right"), Interval(-0.001, 2, closed="right")],
        index=[0, 1, 2, 3, 0],
        dtype="category",
    ).cat.as_ordered()

    ser = Series([0, 1, 2, 3, 0], index=[0, 1, 2, 3, 0])
    result = cut(ser, bins=[0, 2, 4], include_lowest=True)
    tm.assert_series_equal(result, expected)

