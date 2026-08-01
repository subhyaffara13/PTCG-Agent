
def test_from_arrow_from_empty(unit, tz):
    pa = pytest.importorskip("pyarrow")

    data = []
    arr = pa.array(data)
    dtype = DatetimeTZDtype(unit=unit, tz=tz)

    result = dtype.__from_arrow__(arr)
    expected = DatetimeArray._from_sequence(
        np.array(data, dtype=f"datetime64[{unit}]"), dtype=np.dtype(f"M8[{unit}]")
    )
    expected = expected.tz_localize(tz=tz)
    tm.assert_extension_array_equal(result, expected)

    result = dtype.__from_arrow__(pa.chunked_array([arr]))
    tm.assert_extension_array_equal(result, expected)

