
def test_to_datetime_format_f_parse_nanos():
    # GH 48767
    timestamp = "15/02/2020 02:03:04.123456789"
    timestamp_format = "%d/%m/%Y %H:%M:%S.%f"
    result = to_datetime(timestamp, format=timestamp_format)
    expected = Timestamp(
        year=2020,
        month=2,
        day=15,
        hour=2,
        minute=3,
        second=4,
        microsecond=123456,
        nanosecond=789,
    )
    assert result == expected

