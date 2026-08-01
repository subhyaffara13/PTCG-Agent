
def test_compression_binary(compression_only, temp_file):
    """
    Binary file handles support compression.

    GH22555
    """
    df = pd.DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=pd.Index(list("ABCD")),
        index=pd.Index([f"i-{i}" for i in range(30)]),
    )

    # with a file
    path = temp_file
    with open(path, mode="wb") as file:
        df.to_csv(file, mode="wb", compression=compression_only)
        file.seek(0)  # file shouldn't be closed
    tm.assert_frame_equal(
        df, pd.read_csv(path, index_col=0, compression=compression_only)
    )

    # with BytesIO
    file = io.BytesIO()
    df.to_csv(file, mode="wb", compression=compression_only)
    file.seek(0)  # file shouldn't be closed
    tm.assert_frame_equal(
        df, pd.read_csv(file, index_col=0, compression=compression_only)
    )

