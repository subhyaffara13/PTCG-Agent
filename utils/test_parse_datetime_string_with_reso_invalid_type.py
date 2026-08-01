
def test_parse_datetime_string_with_reso_invalid_type():
    # Raise on invalid input, don't just return it
    msg = "Argument 'date_string' has incorrect type (expected str, got tuple)"
    with pytest.raises(TypeError, match=re.escape(msg)):
        parse_datetime_string_with_reso((4, 5))

