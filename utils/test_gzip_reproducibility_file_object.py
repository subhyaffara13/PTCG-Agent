
def test_gzip_reproducibility_file_object():
    """
    Gzip should create reproducible archives with mtime.

    GH 28103
    """
    df = pd.DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=pd.Index(list("ABCD")),
        index=pd.Index([f"i-{i}" for i in range(30)]),
    )
    compression_options = {"method": "gzip", "mtime": 1}

    # test for file object
    buffer = io.BytesIO()
    df.to_csv(buffer, compression=compression_options, mode="wb")
    output = buffer.getvalue()
    buffer = io.BytesIO()
    df.to_csv(buffer, compression=compression_options, mode="wb")
    assert output == buffer.getvalue()

