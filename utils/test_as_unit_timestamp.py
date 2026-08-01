
def test_as_unit_timestamp(from_unit, to_unit):
    # Test timestamp as_unit matches NumPy behavior
    # Create Arrow series directly to preserve nulls correctly
    ser_arrow = pd.Series(
        [pd.Timestamp("2024-01-15 12:30:45.123456789"), None],
        dtype=f"timestamp[{from_unit}][pyarrow]",
    )
    ser_numpy = ser_arrow.astype(f"datetime64[{from_unit}]")

    result = ser_arrow.dt.as_unit(to_unit)
    expected_numpy = ser_numpy.dt.as_unit(to_unit)
    # Compare values (excluding null handling differences)
    tm.assert_almost_equal(
        result.dropna().to_numpy(dtype=f"datetime64[{to_unit}]"),
        expected_numpy.dropna().to_numpy(),
    )
    # Verify nulls are preserved
    assert result.isna().sum() == ser_arrow.isna().sum()

