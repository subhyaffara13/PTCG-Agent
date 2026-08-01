
def test_ambiguous_archive_tar(tmp_path):
    csvAPath = tmp_path / "a.csv"
    with open(csvAPath, "w", encoding="utf-8") as a:
        a.write("foo,bar\n")
    csvBPath = tmp_path / "b.csv"
    with open(csvBPath, "w", encoding="utf-8") as b:
        b.write("foo,bar\n")

    tarpath = tmp_path / "archive.tar"
    with tarfile.TarFile(tarpath, "w") as tar:
        tar.add(csvAPath, "a.csv")
        tar.add(csvBPath, "b.csv")

    with pytest.raises(ValueError, match="Multiple files found in TAR archive"):
        pd.read_csv(tarpath)

