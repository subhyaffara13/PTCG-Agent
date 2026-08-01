
def test_decimal_parse_succeeds():
    # GH 56984
    ser = pd.Series(["1.2345"], dtype=ArrowDtype(pa.string()))
    dtype = ArrowDtype(pa.decimal128(5, 4))
    result = ser.astype(dtype)
    expected = pd.Series([Decimal("1.2345")], dtype=dtype)
    tm.assert_series_equal(result, expected)

