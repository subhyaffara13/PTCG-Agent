
def test_consistency_default_namespace():
    pytest.importorskip("lxml")
    df_lxml = read_xml(
        StringIO(xml_default_nmsp),
        xpath=".//ns:row",
        namespaces={"ns": "http://example.com"},
        parser="lxml",
    )

    df_etree = read_xml(
        StringIO(xml_default_nmsp),
        xpath=".//doc:row",
        namespaces={"doc": "http://example.com"},
        parser="etree",
    )

    tm.assert_frame_equal(df_lxml, df_etree)

