
def test_wrong_dict_type(xml_books, parser):
    with pytest.raises(TypeError, match="list is not a valid type for iterparse"):
        read_xml(
            xml_books,
            parser=parser,
            iterparse=["category", "title", "year", "author", "price"],
        )

