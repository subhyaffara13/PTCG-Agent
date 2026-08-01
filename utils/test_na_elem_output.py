
def test_na_elem_output(parser, geom_df):
    output = geom_df.to_xml(parser=parser)
    output = equalize_decl(output)

    assert output == na_expected

