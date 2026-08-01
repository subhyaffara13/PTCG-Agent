
def test_duration_overflow_from_ndarray_containing_nat():
    # GH52843
    data_ts = pd.to_datetime([1, None])
    data_td = pd.to_timedelta([1, None])
    ser_ts = pd.Series(data_ts, dtype=ArrowDtype(pa.timestamp("ns")))
    ser_td = pd.Series(data_td, dtype=ArrowDtype(pa.duration("ns")))
    result = ser_ts + ser_td
    expected = pd.Series([2, None], dtype=ArrowDtype(pa.timestamp("ns")))
    tm.assert_series_equal(result, expected)

