
def test_convert_dtypes_infer_objects():
    ser = Series(["a", "b", "c"])
    ser_orig = ser.copy()
    result = ser.convert_dtypes(
        convert_integer=False,
        convert_boolean=False,
        convert_floating=False,
        convert_string=False,
    )

    assert tm.shares_memory(get_array(ser), get_array(result))
    result.iloc[0] = "x"
    tm.assert_series_equal(ser, ser_orig)

