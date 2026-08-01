
def test_na_empty_str_elem_option(parser, geom_df):
    output = geom_df.to_xml(na_rep="", parser=parser)
    output = equalize_decl(output)

    assert output == na_expected

