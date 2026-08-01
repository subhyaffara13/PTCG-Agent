
def test_comment_whitespace_delimited(c_parser_only):
    parser = c_parser_only
    test_input = """\
1 2
2 2 3
3 2 3 # 3 fields
4 2 3# 3 fields
5 2 # 2 fields
6 2# 2 fields
7 # 1 field, NaN
8# 1 field, NaN
9 2 3 # skipped line
# comment"""
    with tm.assert_produces_warning(
        ParserWarning, match="Skipping line", check_stacklevel=False
    ):
        df = parser.read_csv(
            StringIO(test_input),
            comment="#",
            header=None,
            delimiter="\\s+",
            skiprows=0,
            on_bad_lines="warn",
        )
    expected = DataFrame([[1, 2], [5, 2], [6, 2], [7, np.nan], [8, np.nan]])
    tm.assert_frame_equal(df, expected)

