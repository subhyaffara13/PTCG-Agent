
def test_pickle_binary_object_compression(compression, temp_file):
    """
    Read/write from binary file-objects w/wo compression.

    GH 26237, GH 29054, and GH 29570
    """
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )

    # reference for compression
    path = temp_file
    df.to_pickle(path, compression=compression)
    reference = path.read_bytes()

    # write
    buffer = io.BytesIO()
    df.to_pickle(buffer, compression=compression)
    buffer.seek(0)

    # gzip  and zip safe the filename: cannot compare the compressed content
    assert buffer.getvalue() == reference or compression in ("gzip", "zip", "tar")

    # read
    read_df = pd.read_pickle(buffer, compression=compression)
    buffer.seek(0)
    tm.assert_frame_equal(df, read_df)

