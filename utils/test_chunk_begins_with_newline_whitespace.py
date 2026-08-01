
def test_chunk_begins_with_newline_whitespace(all_parsers):
    # see gh-10022
    parser = all_parsers
    data = "\n hello\nworld\n"

    result = parser.read_csv(StringIO(data), header=None)
    expected = DataFrame([" hello", "world"])
    tm.assert_frame_equal(result, expected)

