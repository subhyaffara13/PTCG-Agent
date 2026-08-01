
def test_index_false_rename_row_root(xml_books, parser, temp_file):
    expected = """\
<?xml version='1.0' encoding='utf-8'?>
<books>
  <book>
    <category>cooking</category>
    <title>Everyday Italian</title>
    <author>Giada De Laurentiis</author>
    <year>2005</year>
    <price>30.0</price>
  </book>
  <book>
    <category>children</category>
    <title>Harry Potter</title>
    <author>J K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
  <book>
    <category>web</category>
    <title>Learning XML</title>
    <author>Erik T. Ray</author>
    <year>2003</year>
    <price>39.95</price>
  </book>
</books>"""

    df_file = read_xml(xml_books, parser=parser)

    df_file.to_xml(
        temp_file, index=False, root_name="books", row_name="book", parser=parser
    )
    output = temp_file.read_text(encoding="utf-8").strip()

    output = equalize_decl(output)

    assert output == expected

