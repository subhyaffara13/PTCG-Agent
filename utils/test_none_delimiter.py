
def test_none_delimiter(python_parser_only):
    # see gh-13374 and gh-17465
    parser = python_parser_only
    data = "a,b,c\n0,1,2\n3,4,5,6\n7,8,9"
    expected = DataFrame({"a": [0, 7], "b": [1, 8], "c": [2, 9]})

    # We expect the third line in the data to be
    # skipped because it is malformed, but we do
    # not expect any errors to occur.
    with tm.assert_produces_warning(
        ParserWarning, match="Skipping line 3", check_stacklevel=False
    ):
        result = parser.read_csv(
            StringIO(data), header=0, sep=None, on_bad_lines="warn"
        )
    tm.assert_frame_equal(result, expected)

