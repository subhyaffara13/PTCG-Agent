
def test_header_int_do_not_infer_multiindex_names_on_different_line(python_parser_only):
    # GH#46569
    parser = python_parser_only
    data = StringIO("a\na,b\nc,d,e\nf,g,h")
    result = parser.read_csv_check_warnings(
        ParserWarning, "Length of header", data, engine="python", index_col=False
    )
    expected = DataFrame({"a": ["a", "c", "f"]})
    tm.assert_frame_equal(result, expected)

