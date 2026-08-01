
def test_wrong_converters_type(xml_books, parser, iterparse):
    with pytest.raises(TypeError, match=("Type converters must be a dict or subclass")):
        read_xml(
            xml_books, converters={"year", str}, parser=parser, iterparse=iterparse
        )

