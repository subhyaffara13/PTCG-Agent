
def test_compression_tar_archive(all_parsers, csv_dir_path):
    parser = all_parsers
    path = os.path.join(csv_dir_path, "tar_csv.tar.gz")
    df = parser.read_csv(path)
    assert list(df.columns) == ["a"]

