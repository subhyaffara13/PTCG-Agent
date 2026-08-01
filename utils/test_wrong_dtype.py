
def test_wrong_dtype(xml_books, parser, iterparse):
    with pytest.raises(
        ValueError, match=('Unable to parse string "Everyday Italian" at position 0')
    ):
        read_xml(
            xml_books, dtype={"title": "Int64"}, parser=parser, iterparse=iterparse
        )

