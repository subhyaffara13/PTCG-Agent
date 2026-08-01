
def test_read_from_pathlib_path(temp_h5_path):
    # GH11773
    expected = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )

    expected.to_hdf(temp_h5_path, key="df", mode="a")
    actual = read_hdf(temp_h5_path, key="df")

    tm.assert_frame_equal(expected, actual)

