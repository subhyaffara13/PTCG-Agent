
def test_sniff_delimiter_comment(python_parser_only):
    data = """# comment line
index|A|B|C
# comment line
foo|1|2|3 # ignore | this
bar|4|5|6
baz|7|8|9
"""
    parser = python_parser_only
    result = parser.read_csv(StringIO(data), index_col=0, sep=None, comment="#")
    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        columns=["A", "B", "C"],
        index=Index(["foo", "bar", "baz"], name="index"),
    )
    tm.assert_frame_equal(result, expected)

