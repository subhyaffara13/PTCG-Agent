
def test_cut_bins_datetime_intervalindex():
    # https://github.com/pandas-dev/pandas/issues/46218
    bins = interval_range(Timestamp("2022-02-25"), Timestamp("2022-02-27"), freq="1D")
    # passing Series instead of list is important to trigger bug
    result = cut(Series([Timestamp("2022-02-26")]), bins=bins)
    expected = Categorical.from_codes([0], bins, ordered=True)
    tm.assert_categorical_equal(result.array, expected)

