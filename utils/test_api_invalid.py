
def test_api_invalid(temp_h5_path):
    path = temp_h5_path
    # Invalid.
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    msg = "Can only append to Tables"

    with pytest.raises(ValueError, match=msg):
        df.to_hdf(path, key="df", append=True, format="f")

    with pytest.raises(ValueError, match=msg):
        df.to_hdf(path, key="df", append=True, format="fixed")

    msg = r"invalid HDFStore format specified \[foo\]"

    with pytest.raises(TypeError, match=msg):
        df.to_hdf(path, key="df", append=True, format="foo")

    with pytest.raises(TypeError, match=msg):
        df.to_hdf(path, key="df", append=False, format="foo")

    # File path doesn't exist
    path = ""
    msg = f"File {path} does not exist"

    with pytest.raises(FileNotFoundError, match=msg):
        read_hdf(path, "df")

