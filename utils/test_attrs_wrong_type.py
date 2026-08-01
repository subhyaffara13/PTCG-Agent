
def test_attrs_wrong_type(parser, geom_df):
    with pytest.raises(TypeError, match=("is not a valid type for attr_cols")):
        geom_df.to_xml(attr_cols='"shape", "degree", "sides"', parser=parser)

