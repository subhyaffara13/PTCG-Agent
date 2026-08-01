
def test_callable_func_converters(xml_books, parser, iterparse):
    with pytest.raises(TypeError, match=("'float' object is not callable")):
        read_xml(
            xml_books, converters={"year": float()}, parser=parser, iterparse=iterparse
        )

