
def test_ignore_compression_extension(tmp_path, all_parsers):
    parser = all_parsers
    df = DataFrame({"a": [0, 1]})

    path_csv = tmp_path / "test.csv"
    path_zip = tmp_path / "test.csv.zip"
    # make sure to create un-compressed file with zip extension
    df.to_csv(path_csv, index=False)
    Path(path_zip).write_text(
        Path(path_csv).read_text(encoding="utf-8"), encoding="utf-8"
    )

    tm.assert_frame_equal(parser.read_csv(path_zip, compression=None), df)

