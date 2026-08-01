
def test_binary_mode_file_buffers(all_parsers, file_path, encoding, datapath):
    # gh-23779: Python csv engine shouldn't error on files opened in binary.
    # gh-31575: Python csv engine shouldn't error on files opened in raw binary.
    parser = all_parsers

    fpath = datapath(*file_path)
    expected = parser.read_csv(fpath, encoding=encoding)

    with open(fpath, encoding=encoding) as fa:
        result = parser.read_csv(fa)
        assert not fa.closed
    tm.assert_frame_equal(expected, result)

    with open(fpath, mode="rb") as fb:
        result = parser.read_csv(fb, encoding=encoding)
        assert not fb.closed
    tm.assert_frame_equal(expected, result)

    with open(fpath, mode="rb", buffering=0) as fb:
        result = parser.read_csv(fb, encoding=encoding)
        assert not fb.closed
    tm.assert_frame_equal(expected, result)

