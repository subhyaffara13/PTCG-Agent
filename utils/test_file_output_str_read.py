
def test_file_output_str_read(xml_books, parser, from_file_expected, temp_file):
    df_file = read_xml(xml_books, parser=parser)

    df_file.to_xml(temp_file, parser=parser)
    output = temp_file.read_text(encoding="utf-8").strip()

    output = equalize_decl(output)

    assert output == from_file_expected

