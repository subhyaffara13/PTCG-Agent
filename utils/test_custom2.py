
def test_custom2():
    # Makes the parser parse commas as the decimal separator instead of dots

    parser = init_custom_parser(modification2, CustomTransformer)

    with raises(lark.exceptions.UnexpectedCharacters):
        # Asserting that the default parser cannot parse numbers which have commas as
        # the decimal separator
        parse_latex_lark("100,1")
        parse_latex_lark("0,009")

    parser.doparse("100,1")
    parser.doparse("0,009")
    parser.doparse("2,71828")
    parser.doparse("3,14159")

