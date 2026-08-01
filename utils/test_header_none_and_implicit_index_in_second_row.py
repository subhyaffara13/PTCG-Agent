
def test_header_none_and_implicit_index_in_second_row(all_parsers):
    # GH#22144
    parser = all_parsers
    data = "x,1\ny,2,5\nz,3\n"
    with pytest.raises(ParserError, match="Expected 2 fields in line 2, saw 3"):
        parser.read_csv(StringIO(data), names=["a", "b"], header=None)

