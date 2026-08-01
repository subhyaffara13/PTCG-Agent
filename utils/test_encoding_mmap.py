
def test_encoding_mmap(memory_map, temp_file):
    """
    encoding should be working, even when using a memory-mapped file.

    GH 23254.
    """
    encoding = "iso8859_1"
    path = temp_file
    path.write_bytes(" 1 A Ä 2\n".encode(encoding))
    df = read_fwf(
        path,
        header=None,
        widths=[2, 2, 2, 2],
        encoding=encoding,
        memory_map=memory_map,
    )
    df_reference = DataFrame([[1, "A", "Ä", 2]])
    tm.assert_frame_equal(df, df_reference)

