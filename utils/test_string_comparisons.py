
def test_string_comparisons(op, ufunc, sym, dtypes, aligned):
    # ensure native byte-order for the first view to stay within unicode range
    native_dt = np.dtype(dtypes[0]).newbyteorder("=")
    arr = np.arange(2**15).view(native_dt).astype(dtypes[0])
    if not aligned:
        # Make `arr` unaligned:
        new = np.zeros(arr.nbytes + 1, dtype=np.uint8)[1:].view(dtypes[0])
        new[...] = arr
        arr = new

    arr2 = arr.astype(dtypes[1], copy=True)
    np.random.shuffle(arr2)
    arr[0] = arr2[0]  # make sure one matches

    expected = [op(d1, d2) for d1, d2 in zip(arr.tolist(), arr2.tolist())]
    assert_array_equal(op(arr, arr2), expected)
    assert_array_equal(ufunc(arr, arr2), expected)
    assert_array_equal(
        np.char.compare_chararrays(arr, arr2, sym, False), expected
    )

    expected = [op(d2, d1) for d1, d2 in zip(arr.tolist(), arr2.tolist())]
    assert_array_equal(op(arr2, arr), expected)
    assert_array_equal(ufunc(arr2, arr), expected)
    assert_array_equal(
        np.char.compare_chararrays(arr2, arr, sym, False), expected
    )

