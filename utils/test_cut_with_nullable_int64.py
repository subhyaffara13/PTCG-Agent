
def test_cut_with_nullable_int64():
    # GH 30787
    series = Series([0, 1, 2, 3, 4, pd.NA, 6, 7], dtype="Int64")
    bins = [0, 2, 4, 6, 8]
    intervals = IntervalIndex.from_breaks(bins)

    expected = Series(
        Categorical.from_codes([-1, 0, 0, 1, 1, -1, 2, 3], intervals, ordered=True)
    )

    result = cut(series, bins=bins)

    tm.assert_series_equal(result, expected)

