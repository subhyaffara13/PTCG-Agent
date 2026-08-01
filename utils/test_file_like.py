
def test_file_like(xml_books, parser, mode):
    with open(xml_books, mode, encoding="utf-8" if mode == "r" else None) as f:
        df_file = read_xml(f, parser=parser)

    df_expected = DataFrame(
        {
            "category": ["cooking", "children", "web"],
            "title": ["Everyday Italian", "Harry Potter", "Learning XML"],
            "author": ["Giada De Laurentiis", "J K. Rowling", "Erik T. Ray"],
            "year": [2005, 2005, 2003],
            "price": [30.00, 29.99, 39.95],
        }
    )

    tm.assert_frame_equal(df_file, df_expected)

