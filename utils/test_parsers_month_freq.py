
def test_parsers_month_freq(date_str, expected):
    result, _ = parsing.parse_datetime_string_with_reso(date_str, freq="ME")
    assert result == expected

