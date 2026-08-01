
def test_astype_copyflag():
    # test the various copyflag options
    arr = np.arange(10, dtype=np.intp)

    res_true = arr.astype(np.intp, copy=True)
    assert not np.shares_memory(arr, res_true)

    res_false = arr.astype(np.intp, copy=False)
    assert np.shares_memory(arr, res_false)

    res_false_float = arr.astype(np.float64, copy=False)
    assert not np.shares_memory(arr, res_false_float)

    # _CopyMode enum isn't allowed
    assert_raises(ValueError, arr.astype, np.float64,
                  copy=np._CopyMode.NEVER)

