
def test_from_arrow_with_different_units_and_timezones_with(
    pa_unit, pd_unit, pa_tz, pd_tz, data
):
    pa = pytest.importorskip("pyarrow")

    pa_type = pa.timestamp(pa_unit, tz=pa_tz)
    arr = pa.array(data, type=pa_type)
    dtype = DatetimeTZDtype(unit=pd_unit, tz=pd_tz)

    result = dtype.__from_arrow__(arr)
    expected = DatetimeArray._from_sequence(data, dtype=f"M8[{pa_unit}, UTC]").astype(
        dtype, copy=False
    )
    tm.assert_extension_array_equal(result, expected)

    result = dtype.__from_arrow__(pa.chunked_array([arr]))
    tm.assert_extension_array_equal(result, expected)

