
def test_read_csv_multi_header_length_check(all_parsers):
    # GH#43102
    parser = all_parsers

    case = """row11,row12,row13
row21,row22, row23
row31,row32
"""

    with pytest.raises(
        ParserError, match="Header rows must have an equal number of columns."
    ):
        parser.read_csv(StringIO(case), header=[0, 2])

