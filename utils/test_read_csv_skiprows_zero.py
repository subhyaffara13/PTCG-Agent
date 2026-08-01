
def test_read_csv_skiprows_zero(python_parser_only):
    # GH 62739
    tbl = """\
"
a b
1 3
"""
    parser = python_parser_only
    # don't skip anything
    with pytest.raises(ParserError, match="unexpected end of data"):
        parser.read_csv(StringIO(tbl), delimiter=" ", skiprows=0, engine="python")

