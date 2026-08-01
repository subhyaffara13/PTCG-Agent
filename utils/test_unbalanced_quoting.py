
def test_unbalanced_quoting(all_parsers, balanced, request):
    # see gh-22789.
    parser = all_parsers
    data = 'a,b,c\n1,2,"3'

    if parser.engine == "pyarrow" and not balanced:
        mark = pytest.mark.xfail(reason="Mismatched result")
        request.applymarker(mark)

    if balanced:
        # Re-balance the quoting and read in without errors.
        expected = DataFrame([[1, 2, 3]], columns=["a", "b", "c"])
        result = parser.read_csv(StringIO(data + '"'))
        tm.assert_frame_equal(result, expected)
    else:
        msg = (
            "EOF inside string starting at row 1"
            if parser.engine == "c"
            else "unexpected end of data"
        )

        with pytest.raises(ParserError, match=msg):
            parser.read_csv(StringIO(data))

