
def test_zip(tmp_path, parser_and_data, compression):
    parser, data, expected = parser_and_data

    path = tmp_path / "test_file.zip"
    with zipfile.ZipFile(path, mode="w") as tmp:
        tmp.writestr("test_file", data)

    if compression == "zip2":
        with open(path, "rb") as f:
            result = parser.read_csv(f, compression="zip")
    else:
        result = parser.read_csv(path, compression=compression)

    tm.assert_frame_equal(result, expected)

