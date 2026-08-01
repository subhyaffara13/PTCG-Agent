
def test_parse_datetime_string_with_reso():
    (parsed, reso) = parse_datetime_string_with_reso("4Q1984")
    (parsed_lower, reso_lower) = parse_datetime_string_with_reso("4q1984")

    assert reso == reso_lower
    assert parsed == parsed_lower

