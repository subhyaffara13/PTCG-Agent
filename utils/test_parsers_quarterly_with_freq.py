
def test_parsers_quarterly_with_freq(date_str, freq, expected):
    result, _ = parsing.parse_datetime_string_with_reso(date_str, freq=freq)
    assert result == expected

