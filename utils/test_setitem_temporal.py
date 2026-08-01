
def test_setitem_temporal(pa_type):
    # GH 53171
    unit = pa_type.unit
    if pa.types.is_duration(pa_type):
        val = pd.Timedelta(1, unit=unit).as_unit(unit)
    else:
        val = pd.Timestamp(1, unit=unit, tz=pa_type.tz).as_unit(unit)

    arr = ArrowExtensionArray(pa.array([1, 2, 3], type=pa_type))

    result = arr.copy()
    result[:] = val
    expected = ArrowExtensionArray(pa.array([1, 1, 1], type=pa_type))
    tm.assert_extension_array_equal(result, expected)

