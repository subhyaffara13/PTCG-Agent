
def test_compression_roundtrip(compression, temp_file):
    df = DataFrame(
        [[0.123456, 0.234567, 0.567567], [12.32112, 123123.2, 321321.2]],
        index=["A", "B"],
        columns=["X", "Y", "Z"],
    )
    df.index.name = "index"

    df.to_stata(temp_file, compression=compression)
    reread = read_stata(temp_file, compression=compression, index_col="index")
    tm.assert_frame_equal(df, reread)

    # explicitly ensure file was compressed.
    with tm.decompress_file(temp_file, compression) as fh:
        contents = io.BytesIO(fh.read())
    reread = read_stata(contents, index_col="index")
    tm.assert_frame_equal(df, reread)


def test_compression_roundtrip(compression, temp_file):
    df = pd.DataFrame(
        [[0.123456, 0.234567, 0.567567], [12.32112, 123123.2, 321321.2]],
        index=["A", "B"],
        columns=["X", "Y", "Z"],
    )

    df.to_json(temp_file, compression=compression)
    tm.assert_frame_equal(df, pd.read_json(temp_file, compression=compression))

    # explicitly ensure file was compressed.
    with tm.decompress_file(temp_file, compression) as fh:
        result = fh.read().decode("utf8")
        data = StringIO(result)
    tm.assert_frame_equal(df, pd.read_json(data))

