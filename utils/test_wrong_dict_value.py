
def test_wrong_dict_value(xml_books, parser):
    with pytest.raises(
        TypeError, match="<class 'str'> is not a valid type for value in iterparse"
    ):
        read_xml(xml_books, parser=parser, iterparse={"book": "category"})

