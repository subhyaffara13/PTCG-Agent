
def test_zip_error_no_files(tmp_path, parser_and_data):
    parser, _, _ = parser_and_data

    path = tmp_path / "test_file.zip"
    with zipfile.ZipFile(path, mode="w"):
        pass

    with pytest.raises(ValueError, match="Zero files"):
        parser.read_csv(path, compression="zip")

