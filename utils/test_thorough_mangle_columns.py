
def test_thorough_mangle_columns(all_parsers, data, expected):
    # see gh-17060
    parser = all_parsers

    result = parser.read_csv(StringIO(data))
    tm.assert_frame_equal(result, expected)

