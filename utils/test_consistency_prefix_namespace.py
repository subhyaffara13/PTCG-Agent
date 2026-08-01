
def test_consistency_prefix_namespace():
    pytest.importorskip("lxml")
    df_lxml = read_xml(
        StringIO(xml_prefix_nmsp),
        xpath=".//doc:row",
        namespaces={"doc": "http://example.com"},
        parser="lxml",
    )

    df_etree = read_xml(
        StringIO(xml_prefix_nmsp),
        xpath=".//doc:row",
        namespaces={"doc": "http://example.com"},
        parser="etree",
    )

    tm.assert_frame_equal(df_lxml, df_etree)

