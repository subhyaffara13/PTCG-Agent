
def test_file_buffered_reader_no_xml_declaration(xml_books, parser, mode):
    with open(xml_books, mode, encoding="utf-8" if mode == "r" else None) as f:
        next(f)
        xml_obj = f.read()

    if mode == "rb":
        xml_obj = StringIO(xml_obj.decode())
    elif mode == "r":
        xml_obj = StringIO(xml_obj)

    df_str = read_xml(xml_obj, parser=parser)

    df_expected = DataFrame(
        {
            "category": ["cooking", "children", "web"],
            "title": ["Everyday Italian", "Harry Potter", "Learning XML"],
            "author": ["Giada De Laurentiis", "J K. Rowling", "Erik T. Ray"],
            "year": [2005, 2005, 2003],
            "price": [30.00, 29.99, 39.95],
        }
    )

    tm.assert_frame_equal(df_str, df_expected)

