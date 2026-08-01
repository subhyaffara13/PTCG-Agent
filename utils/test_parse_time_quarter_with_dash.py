
def test_parse_time_quarter_with_dash(dashed, normal):
    # see gh-9688
    (parsed_dash, reso_dash) = parse_datetime_string_with_reso(dashed)
    (parsed, reso) = parse_datetime_string_with_reso(normal)

    assert parsed_dash == parsed
    assert reso_dash == reso

