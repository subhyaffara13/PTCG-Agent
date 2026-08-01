
def test_fillna_interval_inplace_reference():
    # Set dtype explicitly to avoid implicit cast when setting nan
    ser = Series(
        interval_range(start=0, end=5), name="a", dtype="interval[float64, right]"
    )
    ser.iloc[1] = np.nan

    ser_orig = ser.copy()
    view = ser[:]
    ser.fillna(value=Interval(left=0, right=5), inplace=True)

    assert not np.shares_memory(
        get_array(ser, "a").left.values, get_array(view, "a").left.values
    )
    tm.assert_series_equal(view, ser_orig)

