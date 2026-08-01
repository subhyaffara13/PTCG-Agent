
def test_unknown_encoding(xml_baby_names, parser):
    with pytest.raises(LookupError, match=("unknown encoding: UFT-8")):
        read_xml(xml_baby_names, encoding="UFT-8", parser=parser)

