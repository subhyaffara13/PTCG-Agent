
def test_read_csv_leading_quote_skip(python_parser_only):
    # GH 62739
    tbl = """\
    "
a b
1 3
"""
    parser = python_parser_only
    result = parser.read_csv(
        StringIO(tbl),
        delimiter=" ",
        skiprows=1,
    )
    expected = DataFrame({"a": [1], "b": [3]})
    tm.assert_frame_equal(result, expected)

