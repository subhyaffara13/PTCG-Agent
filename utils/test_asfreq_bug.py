
def test_asfreq_bug():
    df = DataFrame(data=[1, 3], index=[timedelta(), timedelta(minutes=3)])
    result = df.resample("1min").asfreq()
    expected = DataFrame(
        data=[1, np.nan, np.nan, 3],
        index=timedelta_range("0 day", periods=4, freq="1min", unit="us"),
    )
    tm.assert_frame_equal(result, expected)

