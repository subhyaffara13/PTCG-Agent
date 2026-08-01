
def test_to_datetime_iso8601_utc_mixed_negative_offset():
    # GH#61389
    data = ["2023-10-15T10:30:00-12:00", "2023-10-15T14:30:00"]
    result = to_datetime(data, utc=True, format="ISO8601")

    expected = DatetimeIndex(
        [Timestamp("2023-10-15 22:30:00+00:00"), Timestamp("2023-10-15 14:30:00+00:00")]
    )
    tm.assert_index_equal(result, expected)

