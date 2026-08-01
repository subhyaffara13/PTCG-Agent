
def test_read_csv_unclosed_double_quote_in_data_still_errors(python_parser_only):
    # GH 62739
    tbl = """\
a b
"
1 3
"""
    parser = python_parser_only
    with pytest.raises(ParserError, match="unexpected end of data"):
        parser.read_csv(StringIO(tbl), delimiter=" ", skiprows=1)

