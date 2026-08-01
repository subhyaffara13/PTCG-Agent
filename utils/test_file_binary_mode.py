
def test_file_binary_mode(c_parser_only, temp_file):
    # see gh-23779
    parser = c_parser_only
    expected = DataFrame([[1, 2, 3], [4, 5, 6]])

    path = temp_file
    with open(path, "w", encoding="utf-8") as f:
        f.write("1,2,3\n4,5,6")

    with open(path, "rb") as f:
        result = parser.read_csv(f, header=None)
        tm.assert_frame_equal(result, expected)

