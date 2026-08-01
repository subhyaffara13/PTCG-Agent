
def test_parsers_quarterly_with_freq_error(date_str, kwargs, msg):
    with pytest.raises(parsing.DateParseError, match=msg):
        parsing.parse_datetime_string_with_reso(date_str, **kwargs)

