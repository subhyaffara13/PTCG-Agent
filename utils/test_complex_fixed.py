
def test_complex_fixed(temp_h5_path):
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)).astype(np.complex64),
        index=list("abcd"),
        columns=list("ABCDE"),
    )

    df.to_hdf(temp_h5_path, key="df")
    reread = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df, reread)

    df = DataFrame(
        np.random.default_rng(2).random((4, 5)).astype(np.complex128),
        index=list("abcd"),
        columns=list("ABCDE"),
    )
    df.to_hdf(temp_h5_path, key="df")
    reread = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df, reread)

