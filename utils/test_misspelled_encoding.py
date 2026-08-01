
def test_misspelled_encoding(parser, geom_df):
    with pytest.raises(LookupError, match=("unknown encoding")):
        geom_df.to_xml(encoding="uft-8", parser=parser)

