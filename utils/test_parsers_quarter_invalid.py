
def test_parsers_quarter_invalid(date_str):
    if date_str == "6Q-20":
        msg = (
            "Incorrect quarterly string is given, quarter "
            f"must be between 1 and 4: {date_str}"
        )
    else:
        msg = f"Unknown datetime string format, unable to parse: {date_str}"

    with pytest.raises(ValueError, match=msg):
        parsing.parse_datetime_string_with_reso(date_str)

