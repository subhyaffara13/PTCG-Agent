
def test_series_numeric(data):
    ser = Series(data, index=list("ABCD"), name="EFG")

    result = to_numeric(ser)
    tm.assert_series_equal(result, ser)

