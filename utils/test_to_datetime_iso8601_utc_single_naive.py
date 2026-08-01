
def test_to_datetime_iso8601_utc_single_naive():
    # GH#61389
    result = to_datetime("2023-10-15T14:30:00", utc=True, format="ISO8601")
    expected = Timestamp("2023-10-15 14:30:00+00:00")
    assert result == expected

