
def test_rolling_descending_date_order_with_offset(frame_or_series):
    # GH#40002
    msg = "'d' is deprecated and will be removed in a future version."

    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        idx = date_range(start="2020-01-01", end="2020-01-03", freq="1d")
        obj = frame_or_series(range(1, 4), index=idx)
        result = obj.rolling("1d", closed="left").sum()

    expected = frame_or_series([np.nan, 1, 2], index=idx)
    tm.assert_equal(result, expected)

    result = obj.iloc[::-1].rolling("1D", closed="left").sum()
    idx = date_range(start="2020-01-03", end="2020-01-01", freq="-1D")
    expected = frame_or_series([np.nan, 3, 2], index=idx)
    tm.assert_equal(result, expected)

