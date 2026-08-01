
def test_encoding_option_str(xml_baby_names, parser):
    df_file = read_xml(xml_baby_names, parser=parser, encoding="ISO-8859-1").head(5)

    output = df_file.to_xml(encoding="ISO-8859-1", parser=parser)

    if output is not None:
        # etree and lxml differ on quotes and case in xml declaration
        output = output.replace(
            '<?xml version="1.0" encoding="ISO-8859-1"?',
            "<?xml version='1.0' encoding='ISO-8859-1'?",
        )

    assert output == encoding_expected

