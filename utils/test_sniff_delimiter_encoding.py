
def test_sniff_delimiter_encoding(python_parser_only, encoding):
    parser = python_parser_only
    data = """ignore this
ignore this too
index|A|B|C
foo|1|2|3
bar|4|5|6
baz|7|8|9
"""

    if encoding is not None:
        data = data.encode(encoding)
        data = BytesIO(data)
        data = TextIOWrapper(data, encoding=encoding)
    else:
        data = StringIO(data)

    result = parser.read_csv(data, index_col=0, sep=None, skiprows=2, encoding=encoding)
    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        columns=["A", "B", "C"],
        index=Index(["foo", "bar", "baz"], name="index"),
    )
    tm.assert_frame_equal(result, expected)

