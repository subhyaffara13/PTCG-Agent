
def test_missing_prefix_in_nmsp(parser, geom_df):
    with pytest.raises(KeyError, match=("doc is not included in namespaces")):
        geom_df.to_xml(
            namespaces={"": "http://example.com"}, prefix="doc", parser=parser
        )

