
def test_to_datetime_monotonic_increasing_index(cache):
    # GH28238
    cstart = start_caching_at
    times = date_range(Timestamp("1980"), periods=cstart, freq="YS")
    times = times.to_frame(index=False, name="DT").sample(n=cstart, random_state=1)
    times.index = times.index.to_series().astype(float) / 1000
    result = to_datetime(times.iloc[:, 0], cache=cache)
    expected = times.iloc[:, 0]
    tm.assert_series_equal(result, expected)

