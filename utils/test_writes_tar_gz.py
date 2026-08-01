
def test_writes_tar_gz(tmp_path, all_parsers):
    parser = all_parsers
    data = DataFrame(
        {
            "Country": ["Venezuela", "Venezuela"],
            "Twitter": ["Hugo Chávez Frías", "Henrique Capriles R."],
        }
    )
    tar_path = tmp_path / "test.tar.gz"
    data.to_csv(tar_path, index=False)

    # test that read_csv infers .tar.gz to gzip:
    tm.assert_frame_equal(parser.read_csv(tar_path), data)

    # test that file is indeed gzipped:
    with tarfile.open(tar_path, "r:gz") as tar:
        result = parser.read_csv(
            tar.extractfile(tar.getnames()[0]), compression="infer"
        )
        tm.assert_frame_equal(result, data)

