
def test_wrong_encoding(xml_baby_names, parser):
    with pytest.raises(UnicodeDecodeError, match=("'utf-8' codec can't decode")):
        read_xml(xml_baby_names, parser=parser)

