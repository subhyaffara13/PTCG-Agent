
def test_sniff_delimiter(python_parser_only, kwargs):
    data = """index|A|B|C
foo|1|2|3
bar|4|5|6
baz|7|8|9
"""
    parser = python_parser_only
    result = parser.read_csv(StringIO(data), index_col=0, **kwargs)
    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        columns=["A", "B", "C"],
        index=Index(["foo", "bar", "baz"], name="index"),
    )
    tm.assert_frame_equal(result, expected)

