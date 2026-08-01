
def test_ufunc_add_reduce(dtype):
    values = ["a", "this is a long string", "c"]
    arr = np.array(values, dtype=dtype)
    out = np.empty((), dtype=dtype)

    expected = np.array("".join(values), dtype=dtype)
    assert_array_equal(np.add.reduce(arr), expected)

    np.add.reduce(arr, out=out)
    assert_array_equal(out, expected)

