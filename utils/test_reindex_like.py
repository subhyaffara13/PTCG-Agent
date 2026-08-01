
def test_reindex_like():
    df = DataFrame({"a": [1, 2], "b": "a"})
    other = DataFrame({"b": "a", "a": [1, 2]})

    df_orig = df.copy()
    df2 = df.reindex_like(other)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df2.iloc[0, 1] = 0
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)


def test_reindex_like(datetime_series):
    other = datetime_series[::2]
    tm.assert_series_equal(
        datetime_series.reindex(other.index), datetime_series.reindex_like(other)
    )

    # GH#7179
    day1 = datetime(2013, 3, 5)
    day2 = datetime(2013, 5, 5)
    day3 = datetime(2014, 3, 5)

    series1 = Series([5, None, None], [day1, day2, day3])
    series2 = Series([None, None], [day1, day3])

    with tm.assert_produces_warning(Pandas4Warning):
        result = series1.reindex_like(series2, method="pad")
    expected = Series([5, np.nan], index=[day1, day3])
    tm.assert_series_equal(result, expected)

