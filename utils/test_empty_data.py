
def test_empty_data(xml_books, parser):
    with pytest.raises(EmptyDataError, match="No columns to parse from file"):
        read_xml(
            xml_books,
            parser=parser,
            iterparse={"book": ["attr1", "elem1", "elem2", "elem3"]},
        )

