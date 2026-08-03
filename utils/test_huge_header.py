import os

def test_huge_header(tmpdir, mmap_mode):
    f = os.path.join(tmpdir, 'large_header.npy')
    arr = np.array(1, dtype="i," * 10000 + "i")

    with pytest.warns(UserWarning, match=".*format 2.0"):
        np.save(f, arr)

    with pytest.raises(ValueError, match="Header.*large"):
        np.load(f, mmap_mode=mmap_mode)

    with pytest.raises(ValueError, match="Header.*large"):
        np.load(f, mmap_mode=mmap_mode, max_header_size=20000)

    res = np.load(f, mmap_mode=mmap_mode, allow_pickle=True)
    assert_array_equal(res, arr)

    res = np.load(f, mmap_mode=mmap_mode, max_header_size=180000)
    assert_array_equal(res, arr)

