
def test_huge_header_npz(tmpdir):
    f = os.path.join(tmpdir, 'large_header.npz')
    arr = np.array(1, dtype="i," * 10000 + "i")

    with pytest.warns(UserWarning, match=".*format 2.0"):
        np.savez(f, arr=arr)

    # Only getting the array from the file actually reads it
    with pytest.raises(ValueError, match="Header.*large"):
        np.load(f)["arr"]

    with pytest.raises(ValueError, match="Header.*large"):
        np.load(f, max_header_size=20000)["arr"]

    res = np.load(f, allow_pickle=True)["arr"]
    assert_array_equal(res, arr)

    res = np.load(f, max_header_size=180000)["arr"]
    assert_array_equal(res, arr)

