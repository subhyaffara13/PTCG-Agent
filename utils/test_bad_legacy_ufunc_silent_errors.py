
def test_bad_legacy_ufunc_silent_errors():
    # legacy ufuncs can't report errors and NumPy can't check if the GIL
    # is released.  So NumPy has to check after the GIL is released just to
    # cover all bases.  `np.power` uses/used to use this.
    arr = np.arange(3).astype(np.float64)

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error(arr, arr)

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        # not contiguous means the fast-path cannot be taken
        non_contig = arr.repeat(20).reshape(-1, 6)[:, ::2]
        ncu_tests.always_error(non_contig, arr)

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error.outer(arr, arr)

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error.reduce(arr)

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error.reduceat(arr, [0, 1])

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error.accumulate(arr)

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error.at(arr, [0, 1, 2], arr)

