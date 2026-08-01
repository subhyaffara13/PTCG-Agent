
def test_resample_depr_lowercase_frequency(freq, freq_depr, data):
    msg = f"'{freq_depr[1:]}' is deprecated and will be removed in a future version."

    s = Series(range(5), index=date_range("20130101", freq="h", periods=5, unit="ns"))
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        result = s.resample(freq_depr).mean()

    exp_dti = DatetimeIndex(data=data, dtype="datetime64[ns]", freq=freq)
    expected = Series(2.0, index=exp_dti)
    tm.assert_series_equal(result, expected, check_freq=False)

