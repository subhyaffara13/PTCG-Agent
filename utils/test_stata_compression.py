
def test_stata_compression(
    compression_only, read_infer, to_infer, compression_to_extension, tmp_path
):
    compression = compression_only

    ext = compression_to_extension[compression]
    filename = f"test.{ext}"

    df = DataFrame(
        [[0.123456, 0.234567, 0.567567], [12.32112, 123123.2, 321321.2]],
        index=["A", "B"],
        columns=["X", "Y", "Z"],
    )
    df.index.name = "index"

    to_compression = "infer" if to_infer else compression
    read_compression = "infer" if read_infer else compression

    path = tmp_path / filename
    path.touch()
    df.to_stata(path, compression=to_compression)
    result = read_stata(path, compression=read_compression, index_col="index")
    tm.assert_frame_equal(result, df)

