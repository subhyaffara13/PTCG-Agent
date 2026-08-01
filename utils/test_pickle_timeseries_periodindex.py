
def test_pickle_timeseries_periodindex(temp_file):
    # GH#2891
    prng = period_range("1/1/2011", "1/1/2012", freq="M")
    ts = Series(np.random.default_rng(2).standard_normal(len(prng)), prng)
    new_ts = tm.round_trip_pickle(ts, temp_file)
    assert new_ts.index.freqstr == "M"

