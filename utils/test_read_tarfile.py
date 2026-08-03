import os

def test_read_tarfile(c_parser_only, csv_dir_path, tar_suffix):
    # see gh-16530
    #
    # Unfortunately, Python's CSV library can't handle
    # tarfile objects (expects string, not bytes when
    # iterating through a file-like).
    parser = c_parser_only
    tar_path = os.path.join(csv_dir_path, "tar_csv" + tar_suffix)

    with tarfile.open(tar_path, "r") as tar:
        data_file = tar.extractfile("tar_data.csv")

        out = parser.read_csv(data_file)
        expected = DataFrame({"a": [1]})
        tm.assert_frame_equal(out, expected)

