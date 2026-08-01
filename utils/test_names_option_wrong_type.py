
def test_names_option_wrong_type(xml_books, parser):
    with pytest.raises(TypeError, match=("is not a valid type for names")):
        read_xml(xml_books, names="Col1, Col2, Col3", parser=parser)

