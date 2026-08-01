
def test_gzip_reproducibility_file_name(temp_file):
    """
    Gzip should create reproducible archives with mtime.

    Note: Archives created with different filenames will still be different!

    GH 28103
    """
    df = pd.DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=pd.Index(list("ABCD")),
        index=pd.Index([f"i-{i}" for i in range(30)]),
    )
    compression_options = {"method": "gzip", "mtime": 1}

    # test for filename
    path = temp_file
    df.to_csv(path, compression=compression_options)
    output = path.read_bytes()
    df.to_csv(path, compression=compression_options)
    assert output == path.read_bytes()

