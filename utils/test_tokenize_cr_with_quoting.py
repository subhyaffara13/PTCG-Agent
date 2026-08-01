
def test_tokenize_CR_with_quoting(c_parser_only):
    # see gh-3453
    parser = c_parser_only
    data = ' a,b,c\r"a,b","e,d","f,f"'

    result = parser.read_csv(StringIO(data), header=None)
    expected = parser.read_csv(StringIO(data.replace("\r", "\n")), header=None)
    tm.assert_frame_equal(result, expected)

    result = parser.read_csv(StringIO(data))
    expected = parser.read_csv(StringIO(data.replace("\r", "\n")))
    tm.assert_frame_equal(result, expected)

