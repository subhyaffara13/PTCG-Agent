
def test_coerce_outside_ns_bounds(invalid_date, exp_unit, errors):
    arr = np.array([invalid_date], dtype="object")

    result, _ = tslib.array_to_datetime(arr, errors=errors)
    out_reso = np.datetime_data(result.dtype)[0]
    assert out_reso == exp_unit
    ts = Timestamp(invalid_date)
    assert ts.unit == exp_unit

    expected = np.array([ts._value], dtype=f"M8[{exp_unit}]")
    tm.assert_numpy_array_equal(result, expected)

