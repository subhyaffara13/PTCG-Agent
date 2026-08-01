
def test_wrong_parse_dates_type(xml_books, parser, iterparse):
    with pytest.raises(TypeError, match="Only booleans and lists are accepted"):
        read_xml(xml_books, parse_dates={"date"}, parser=parser, iterparse=iterparse)

