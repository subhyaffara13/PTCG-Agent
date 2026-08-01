
def test_metadata_dtype(dt):
    # gh-14142
    arr = np.ones(10, dtype=dt)
    buf = BytesIO()
    with pytest.warns(UserWarning):
        np.save(buf, arr)
    buf.seek(0)

    # Loading should work (metadata was stripped):
    arr2 = np.load(buf)
    # BUG: assert_array_equal does not check metadata
    from numpy.lib._utils_impl import drop_metadata
    assert_array_equal(arr, arr2)
    assert drop_metadata(arr.dtype) is not arr.dtype
    assert drop_metadata(arr2.dtype) is arr2.dtype

