
def test_partial_iteration_error(in_dtype, buf_dtype):
    value = 123  # relies on python cache (leak-check will still find it)
    arr = np.full(int(ncu.BUFSIZE * 2.5), value).astype(in_dtype)
    if in_dtype == "O":
        arr[int(ncu.BUFSIZE * 1.5)] = None
    else:
        arr[int(ncu.BUFSIZE * 1.5)]["f0"] = None

    count = sys.getrefcount(value)

    it = np.nditer(arr, op_dtypes=[np.dtype(buf_dtype)],
            flags=["buffered", "external_loop", "refs_ok"], casting="unsafe")
    with pytest.raises(TypeError):
        # pytest.raises seems to have issues with the error originating
        # in the for loop, so manually unravel:
        next(it)
        next(it)  # raises TypeError

    # Repeat the test with `iternext` after resetting, the buffers should
    # already be cleared from any references, so resetting is sufficient.
    it.reset()
    with pytest.raises(TypeError):
        it.iternext()
        it.iternext()

    assert count == sys.getrefcount(value)

