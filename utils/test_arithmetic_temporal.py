
def test_arithmetic_temporal(pa_type, request):
    # GH 53171
    arr = ArrowExtensionArray(pa.array([1, 2, 3], type=pa_type))
    unit = pa_type.unit
    result = arr - pd.Timedelta(1, unit=unit).as_unit(unit)
    expected = ArrowExtensionArray(pa.array([0, 1, 2], type=pa_type))
    tm.assert_extension_array_equal(result, expected)

