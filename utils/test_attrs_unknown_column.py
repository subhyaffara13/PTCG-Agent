
def test_attrs_unknown_column(parser, geom_df):
    with pytest.raises(KeyError, match=("no valid column")):
        geom_df.to_xml(attr_cols=["shape", "degree", "sides"], parser=parser)

