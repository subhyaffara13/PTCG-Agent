
def test_unknown_parser(geom_df):
    with pytest.raises(
        ValueError, match=("Values for parser can only be lxml or etree.")
    ):
        geom_df.to_xml(parser="bs4")

