
def test_missing_prefix_with_default_namespace(xml_books, parser):
    with pytest.raises(ValueError, match=("xpath does not return any nodes")):
        read_xml(xml_books, xpath=".//Placemark", parser=parser)

