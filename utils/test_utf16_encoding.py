
def test_utf16_encoding(xml_baby_names, parser):
    with pytest.raises(
        UnicodeError,
        match=(
            "UTF-16 stream does not start with BOM|"
            "'utf-16(-le)?' codec can't decode byte"
        ),
    ):
        read_xml(xml_baby_names, encoding="UTF-16", parser=parser)

