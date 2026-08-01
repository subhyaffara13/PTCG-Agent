
def test_duration_from_strings_with_nat(unit):
    # GH51175
    strings = ["1000", "NaT"]
    pa_type = pa.duration(unit)
    dtype = ArrowDtype(pa_type)
    result = ArrowExtensionArray._from_sequence_of_strings(strings, dtype=dtype)
    expected = ArrowExtensionArray(pa.array([1000, None], type=pa_type))
    tm.assert_extension_array_equal(result, expected)

