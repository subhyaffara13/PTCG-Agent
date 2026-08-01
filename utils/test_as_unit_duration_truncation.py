
def test_as_unit_duration_truncation(from_unit, to_unit):
    # Test that as_unit truncates correctly (matches NumPy behavior)
    # Value with sub-unit precision to test truncation
    ser_numpy = pd.Series(
        pd.to_timedelta([93784567890123, None], unit="ns").as_unit(from_unit)
    )
    ser_arrow = ser_numpy.astype(f"duration[{from_unit}][pyarrow]")

    result = ser_arrow.dt.as_unit(to_unit)
    expected = ser_numpy.dt.as_unit(to_unit).astype(f"duration[{to_unit}][pyarrow]")
    tm.assert_series_equal(result, expected)

