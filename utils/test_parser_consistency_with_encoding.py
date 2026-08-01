
def test_parser_consistency_with_encoding(xml_baby_names):
    pytest.importorskip("lxml")
    df_xpath_lxml = read_xml(xml_baby_names, parser="lxml", encoding="ISO-8859-1")
    df_xpath_etree = read_xml(xml_baby_names, parser="etree", encoding="iso-8859-1")

    df_iter_lxml = read_xml(
        xml_baby_names,
        parser="lxml",
        encoding="ISO-8859-1",
        iterparse={"row": ["rank", "malename", "femalename"]},
    )
    df_iter_etree = read_xml(
        xml_baby_names,
        parser="etree",
        encoding="ISO-8859-1",
        iterparse={"row": ["rank", "malename", "femalename"]},
    )

    tm.assert_frame_equal(df_xpath_lxml, df_xpath_etree)
    tm.assert_frame_equal(df_xpath_etree, df_iter_etree)
    tm.assert_frame_equal(df_iter_lxml, df_iter_etree)

