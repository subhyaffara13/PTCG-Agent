
def test_header_delim_whitespace(all_parsers):
    # GH#54918
    parser = all_parsers
    data = """a,b
1,2
3,4
    """
    result = parser.read_csv(StringIO(data), sep=r"\s+")
    expected = DataFrame({"a,b": ["1,2", "3,4"]})
    tm.assert_frame_equal(result, expected)

