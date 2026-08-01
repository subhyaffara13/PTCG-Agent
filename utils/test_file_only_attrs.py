
def test_file_only_attrs(xml_books, parser):
    df_file = read_xml(xml_books, attrs_only=True, parser=parser)
    df_iter = read_xml(xml_books, parser=parser, iterparse={"book": ["category"]})
    df_expected = DataFrame({"category": ["cooking", "children", "web"]})

    tm.assert_frame_equal(df_file, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

