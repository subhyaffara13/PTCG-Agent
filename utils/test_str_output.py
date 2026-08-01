
def test_str_output(xml_books, parser, from_file_expected):
    df_file = read_xml(xml_books, parser=parser)

    output = df_file.to_xml(parser=parser)
    output = equalize_decl(output)

    assert output == from_file_expected

