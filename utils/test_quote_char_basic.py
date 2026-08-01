
def test_quote_char_basic(all_parsers):
    parser = all_parsers
    data = 'a,b,c\n1,2,"cat"'
    expected = DataFrame([[1, 2, "cat"]], columns=["a", "b", "c"])

    result = parser.read_csv(StringIO(data), quotechar='"')
    tm.assert_frame_equal(result, expected)

