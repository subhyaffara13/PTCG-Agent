
def test_as_unit_timestamp_with_timezone(to_unit):
    # Test that timezone is preserved
    ser_numpy = pd.Series(
        pd.to_datetime(["2024-01-15 12:30:45.123456789"])
        .tz_localize("US/Eastern")
        .as_unit("ns")
    )
    ser_arrow = ser_numpy.astype("timestamp[ns, US/Eastern][pyarrow]")

    result = ser_arrow.dt.as_unit(to_unit)
    expected = ser_numpy.dt.as_unit(to_unit).astype(
        f"timestamp[{to_unit}, US/Eastern][pyarrow]"
    )
    tm.assert_series_equal(result, expected)
    assert str(result.dtype) == f"timestamp[{to_unit}, tz=US/Eastern][pyarrow]"

