
def test_elems_wrong_type(parser, geom_df):
    with pytest.raises(TypeError, match=("is not a valid type for elem_cols")):
        geom_df.to_xml(elem_cols='"shape", "degree", "sides"', parser=parser)

