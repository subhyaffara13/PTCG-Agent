
def test_bad_xpath_etree(xml_books):
    with pytest.raises(
        SyntaxError, match=("You have used an incorrect or unsupported XPath")
    ):
        read_xml(xml_books, xpath=".//[book]", parser="etree")

