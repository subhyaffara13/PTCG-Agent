
def test_ascii_encoding(xml_baby_names, parser):
    with pytest.raises(UnicodeDecodeError, match=("'ascii' codec can't decode byte")):
        read_xml(xml_baby_names, encoding="ascii", parser=parser)

