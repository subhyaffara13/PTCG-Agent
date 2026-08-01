
def test_elems_unknown_column(parser, geom_df):
    with pytest.raises(KeyError, match=("no valid column")):
        geom_df.to_xml(elem_cols=["shape", "degree", "sides"], parser=parser)

