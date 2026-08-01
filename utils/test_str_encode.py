
def test_str_encode(errors, encoding, exp):
    ser = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.encode(encoding, errors)
    expected = pd.Series([exp[sys.byteorder], None], dtype=ArrowDtype(pa.binary()))
    tm.assert_series_equal(result, expected)

