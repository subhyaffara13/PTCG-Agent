
def test_names_option_wrong_length(xml_books, parser):
    with pytest.raises(ValueError, match=("names does not match length")):
        read_xml(xml_books, names=["Col1", "Col2", "Col3"], parser=parser)

