
def test_failure_to_convert_uint64_string_to_NaN():
    # GH 32394
    result = to_numeric("uint64", errors="coerce")
    assert np.isnan(result)

    ser = Series([32, 64, np.nan])
    result = to_numeric(Series(["32", "64", "uint64"]), errors="coerce")
    tm.assert_series_equal(result, ser)

