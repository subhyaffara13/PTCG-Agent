
def test_to_datetime_with_empty_str_utc_false_offsets_and_format_mixed():
    # GH#50887, GH#57275
    msg = "Mixed timezones detected. Pass utc=True in to_datetime"

    with pytest.raises(ValueError, match=msg):
        to_datetime(
            ["2020-01-01 00:00+00:00", "2020-01-01 00:00+02:00", ""], format="mixed"
        )

