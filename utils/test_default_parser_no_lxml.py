
def test_default_parser_no_lxml(geom_df):
    with pytest.raises(
        ImportError, match=("lxml not found, please install or use the etree parser.")
    ):
        geom_df.to_xml()


def test_default_parser_no_lxml(xml_books):
    with pytest.raises(
        ImportError, match=("lxml not found, please install or use the etree parser.")
    ):
        read_xml(xml_books)

