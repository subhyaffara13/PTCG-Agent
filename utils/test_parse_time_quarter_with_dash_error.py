
def test_parse_time_quarter_with_dash_error(dashed):
    msg = f"Unknown datetime string format, unable to parse: {dashed}"

    with pytest.raises(parsing.DateParseError, match=msg):
        parse_datetime_string_with_reso(dashed)

