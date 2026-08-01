
def test_read_csv_parse_simple_list(all_parsers):
    parser = all_parsers
    data = """foo
bar baz
qux foo
foo
bar"""

    result = parser.read_csv(StringIO(data), header=None)
    expected = DataFrame(["foo", "bar baz", "qux foo", "foo", "bar"])
    tm.assert_frame_equal(result, expected)

