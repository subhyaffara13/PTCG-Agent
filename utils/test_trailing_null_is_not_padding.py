
def test_trailing_null_is_not_padding():
    arr = np.array(["x\0", "\0", "x\0y\0", "abc"], dtype=StringDType())
    nul = np.array("\0", dtype=StringDType())

    assert_array_equal(np.strings.str_len(arr), [2, 1, 4, 3])
    assert_array_equal(np.strings.find(arr, nul), [1, 0, 1, -1])
    assert_array_equal(np.strings.rfind(arr, nul), [1, 0, 3, -1])
    assert_array_equal(np.strings.count(arr, nul), [1, 1, 2, 0])
    assert_array_equal(np.strings.endswith(arr, nul),
                       [True, True, True, False])
    assert_array_equal(np.strings.slice(arr, -1, None),
                       np.array(["\0", "\0", "\0", "c"],
                                dtype=StringDType()))

