
def test_file_io(xml_books, parser, mode):
    with open(xml_books, mode, encoding="utf-8" if mode == "r" else None) as f:
        xml_obj = f.read()

    df_io = read_xml(
        (BytesIO(xml_obj) if isinstance(xml_obj, bytes) else StringIO(xml_obj)),
        parser=parser,
    )

    df_expected = DataFrame(
        {
            "category": ["cooking", "children", "web"],
            "title": ["Everyday Italian", "Harry Potter", "Learning XML"],
            "author": ["Giada De Laurentiis", "J K. Rowling", "Erik T. Ray"],
            "year": [2005, 2005, 2003],
            "price": [30.00, 29.99, 39.95],
        }
    )

    tm.assert_frame_equal(df_io, df_expected)

