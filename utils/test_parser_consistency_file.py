
def test_parser_consistency_file(xml_books):
    pytest.importorskip("lxml")
    df_file_lxml = read_xml(xml_books, parser="lxml")
    df_file_etree = read_xml(xml_books, parser="etree")

    df_iter_lxml = read_xml(
        xml_books,
        parser="lxml",
        iterparse={"book": ["category", "title", "year", "author", "price"]},
    )
    df_iter_etree = read_xml(
        xml_books,
        parser="etree",
        iterparse={"book": ["category", "title", "year", "author", "price"]},
    )

    tm.assert_frame_equal(df_file_lxml, df_file_etree)
    tm.assert_frame_equal(df_file_lxml, df_iter_lxml)
    tm.assert_frame_equal(df_iter_lxml, df_iter_etree)

