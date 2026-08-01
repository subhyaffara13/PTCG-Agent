
def test_names_option_output(xml_books, parser):
    df_file = read_xml(
        xml_books, names=["Col1", "Col2", "Col3", "Col4", "Col5"], parser=parser
    )
    df_iter = read_xml(
        xml_books,
        parser=parser,
        names=["Col1", "Col2", "Col3", "Col4", "Col5"],
        iterparse={"book": ["category", "title", "author", "year", "price"]},
    )

    df_expected = DataFrame(
        {
            "Col1": ["cooking", "children", "web"],
            "Col2": ["Everyday Italian", "Harry Potter", "Learning XML"],
            "Col3": ["Giada De Laurentiis", "J K. Rowling", "Erik T. Ray"],
            "Col4": [2005, 2005, 2003],
            "Col5": [30.00, 29.99, 39.95],
        }
    )

    tm.assert_frame_equal(df_file, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

