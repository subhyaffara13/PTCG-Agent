
def test_read_seek(all_parsers, tmp_path):
    # GH48646
    parser = all_parsers
    prefix = "### DATA\n"
    content = "nkey,value\ntables,rectangular\n"
    path = tmp_path / "test_seek.csv"
    path.write_text(prefix + content, encoding="utf-8")
    with open(path, encoding="utf-8") as file:
        file.readline()
        actual = parser.read_csv(file)
    expected = parser.read_csv(StringIO(content))
    tm.assert_frame_equal(actual, expected)

