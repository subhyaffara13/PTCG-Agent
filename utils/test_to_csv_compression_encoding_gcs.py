
def test_to_csv_compression_encoding_gcs(
    gcs_buffer, compression_only, encoding, compression_to_extension
):
    """
    Compression and encoding should with GCS.

    GH 35677 (to_csv, compression), GH 26124 (to_csv, encoding), and
    GH 32392 (read_csv, encoding)
    """
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    # reference of compressed and encoded file
    compression = {"method": compression_only}
    if compression_only == "gzip":
        compression["mtime"] = 1  # be reproducible
    buffer = BytesIO()
    df.to_csv(buffer, compression=compression, encoding=encoding, mode="wb")

    # write compressed file with explicit compression
    path_gcs = "gs://test/test.csv"
    df.to_csv(path_gcs, compression=compression, encoding=encoding)
    res = gcs_buffer.getvalue()
    expected = buffer.getvalue()
    assert_equal_zip_safe(res, expected, compression_only)

    read_df = read_csv(
        path_gcs, index_col=0, compression=compression_only, encoding=encoding
    )
    tm.assert_frame_equal(df, read_df)

    # write compressed file with implicit compression
    file_ext = compression_to_extension[compression_only]
    compression["method"] = "infer"
    path_gcs += f".{file_ext}"
    df.to_csv(path_gcs, compression=compression, encoding=encoding)

    res = gcs_buffer.getvalue()
    expected = buffer.getvalue()
    assert_equal_zip_safe(res, expected, compression_only)

    read_df = read_csv(path_gcs, index_col=0, compression="infer", encoding=encoding)
    tm.assert_frame_equal(df, read_df)

