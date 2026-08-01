
def test_wrong_parser(xml_books):
    with pytest.raises(
        ValueError, match=("Values for parser can only be lxml or etree.")
    ):
        read_xml(xml_books, parser="bs4")

