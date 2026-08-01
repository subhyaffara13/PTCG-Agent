
def test_to_pytimedelta_large_values():
    td = Timedelta(1152921504609987375, unit="ns")
    result = td.to_pytimedelta()
    expected = timedelta(days=13343, seconds=86304, microseconds=609987)
    assert result == expected

