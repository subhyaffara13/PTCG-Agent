
def test_astype_different_timezones():
    df = DataFrame(
        {"a": date_range("2019-12-31", periods=5, freq="D", tz="US/Pacific", unit="ns")}
    )
    result = df.astype("datetime64[ns, Europe/Berlin]")
    assert not result._mgr._has_no_reference(0)
    assert np.shares_memory(get_array(df, "a"), get_array(result, "a"))

