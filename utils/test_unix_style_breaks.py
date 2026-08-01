
def test_unix_style_breaks(c_parser_only, temp_file):
    # GH 11020
    parser = c_parser_only
    path = temp_file
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        f.write("blah\n\ncol_1,col_2,col_3\n\n")
    result = parser.read_csv(path, skiprows=2, encoding="utf-8", engine="c")
    expected = DataFrame(columns=["col_1", "col_2", "col_3"])
    tm.assert_frame_equal(result, expected)

