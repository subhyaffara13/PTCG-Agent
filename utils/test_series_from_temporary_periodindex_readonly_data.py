
def test_series_from_temporary_periodindex_readonly_data():
    # GH 63388
    arr = array(["2020-01-01", "2020-01-02"], dtype="period[D]")
    arr._ndarray.flags.writeable = False
    ser = Series(PeriodIndex(arr))
    assert not np.shares_memory(arr._ndarray, get_array(ser))
    ser.iloc[0] = Period("2022-01-01", freq="D")
    expected = Series(
        [Period("2022-01-01", freq="D"), Period("2020-01-02", freq="D")],
        dtype="period[D]",
    )
    tm.assert_series_equal(ser, expected)

