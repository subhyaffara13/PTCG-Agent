
def test_non_nano_dt64_addsub_np_nat_scalars_unsupported_unit():
    # GH 52295
    ser = Series([12332, 23243, 33243], dtype="datetime64[s]")
    result = ser - np.datetime64("nat", "D")
    expected = Series([NaT] * 3, dtype="timedelta64[s]")
    tm.assert_series_equal(result, expected)

    result = ser + np.timedelta64("nat", "D")
    expected = Series([NaT] * 3, dtype="datetime64[s]")
    tm.assert_series_equal(result, expected)

