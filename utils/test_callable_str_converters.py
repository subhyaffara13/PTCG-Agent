
def test_callable_str_converters(xml_books, parser, iterparse):
    with pytest.raises(TypeError, match=("'str' object is not callable")):
        read_xml(
            xml_books, converters={"year": "float"}, parser=parser, iterparse=iterparse
        )

