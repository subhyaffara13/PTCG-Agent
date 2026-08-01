
def test_ambiguous_archive_zip(temp_file):
    path = temp_file.parent / "archive.zip"
    with zipfile.ZipFile(path, "w") as file:
        file.writestr("a.csv", "foo,bar")
        file.writestr("b.csv", "foo,bar")
    with pytest.raises(ValueError, match="Multiple files found in ZIP file"):
        pd.read_csv(path)

