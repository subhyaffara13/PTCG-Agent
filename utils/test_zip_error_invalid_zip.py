
def test_zip_error_invalid_zip(tmp_path, parser_and_data):
    parser, _, _ = parser_and_data

    path = tmp_path / "invalid_file.zip"
    path.touch()
    with open(path, "rb") as f:
        with pytest.raises(zipfile.BadZipFile, match="File is not a zip file"):
            parser.read_csv(f, compression="zip")

