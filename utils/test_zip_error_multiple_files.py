
def test_zip_error_multiple_files(tmp_path, parser_and_data, compression):
    parser, data, expected = parser_and_data

    path = tmp_path / "combined_zip.zip"
    inner_file_names = ["test_file", "second_file"]

    with zipfile.ZipFile(path, mode="w") as tmp:
        for file_name in inner_file_names:
            tmp.writestr(file_name, data)

    with pytest.raises(ValueError, match="Multiple files"):
        parser.read_csv(path, compression=compression)

