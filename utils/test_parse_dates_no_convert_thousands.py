
def test_parse_dates_no_convert_thousands(all_parsers, data, kwargs, expected):
    # see gh-14066
    parser = all_parsers

    result = parser.read_csv(StringIO(data), thousands=".", **kwargs)
    tm.assert_frame_equal(result, expected)

