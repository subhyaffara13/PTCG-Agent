
def test_resample_equivalent_offsets(n1, freq1, n2, freq2, k, unit):
    # GH 24127
    n1_ = n1 * k
    n2_ = n2 * k
    dti = date_range("1991-09-05", "1991-09-06", freq=freq1).as_unit(unit)
    ser = Series(range(len(dti)), index=dti)

    result1 = ser.resample(str(n1_) + freq1).mean()
    result2 = ser.resample(str(n2_) + freq2).mean()
    if freq2 == "D" and isinstance(result2.index.freq, Day):
        # GH#55502 Day is no longer a Tick so no longer compares as equivalent,
        #  but the actual values we expect should still match
        result2.index.freq = to_offset(Timedelta(days=result2.index.freq.n))
    tm.assert_series_equal(result1, result2)

