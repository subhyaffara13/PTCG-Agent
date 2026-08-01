
def test_file_only_elems(xml_books, parser):
    df_file = read_xml(xml_books, elems_only=True, parser=parser)
    df_iter = read_xml(
        xml_books,
        parser=parser,
        iterparse={"book": ["title", "author", "year", "price"]},
    )
    df_expected = DataFrame(
        {
            "title": ["Everyday Italian", "Harry Potter", "Learning XML"],
            "author": ["Giada De Laurentiis", "J K. Rowling", "Erik T. Ray"],
            "year": [2005, 2005, 2003],
            "price": [30.00, 29.99, 39.95],
        }
    )

    tm.assert_frame_equal(df_file, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

