
def test_wrong_encoding_option_lxml(xml_baby_names, parser, encoding, temp_file):
    pytest.importorskip("lxml")
    df_file = read_xml(xml_baby_names, encoding="ISO-8859-1", parser="lxml")

    df_file.to_xml(temp_file, index=False, encoding=encoding, parser=parser)

