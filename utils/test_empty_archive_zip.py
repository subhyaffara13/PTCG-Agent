
def test_empty_archive_zip(suffix, archive, temp_file):
    path = temp_file.parent / f"archive{suffix}"
    with archive(path, "w"):
        pass
    with pytest.raises(ValueError, match="Zero files found"):
        pd.read_csv(path)

