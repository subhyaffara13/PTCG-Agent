
def test_parsers_iso8601_invalid(date_str):
    msg = f'Error parsing datetime string "{date_str}"'

    with pytest.raises(ValueError, match=msg):
        tslib._test_parse_iso8601(date_str)

