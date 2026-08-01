
def test_bad_xpath_lxml(xml_books):
    lxml_etree = pytest.importorskip("lxml.etree")

    with pytest.raises(lxml_etree.XPathEvalError, match=("Invalid expression")):
        read_xml(xml_books, xpath=".//[book]", parser="lxml")

