
def test_read_with_where_tz_aware_index(temp_hdfstore):
    # GH 11926
    periods = 10
    dts = date_range("20151201", periods=periods, freq="D", tz="UTC", unit="ns")
    mi = pd.MultiIndex.from_arrays([dts, range(periods)], names=["DATE", "NO"])
    expected = DataFrame({"MYCOL": 0}, index=mi)

    key = "mykey"
    with pd.HDFStore(temp_hdfstore) as store:
        store.append(key, expected, format="table", append=True)
    result = pd.read_hdf(temp_hdfstore, key, where="DATE > 20151130")
    tm.assert_frame_equal(result, expected)

