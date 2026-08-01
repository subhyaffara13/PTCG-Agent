
def test_empty_xpath_lxml(xml_books):
    pytest.importorskip("lxml")
    with pytest.raises(ValueError, match=("xpath does not return any nodes")):
        read_xml(xml_books, xpath=".//python", parser="lxml")

