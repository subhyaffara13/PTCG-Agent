
def test_invalid_parse_delimited_date(all_parsers, date_string):
    parser = all_parsers
    expected = DataFrame({0: [date_string]}, dtype="str")
    result = parser.read_csv(
        StringIO(date_string),
        header=None,
        parse_dates=[0],
    )
    tm.assert_frame_equal(result, expected)

