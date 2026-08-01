
def test_data_after_quote(c_parser_only):
    # see gh-15910
    parser = c_parser_only

    data = 'a\n1\n"b"a'
    result = parser.read_csv(StringIO(data))

    expected = DataFrame({"a": ["1", "ba"]})
    tm.assert_frame_equal(result, expected)

