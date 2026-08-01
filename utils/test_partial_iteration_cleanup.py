
def test_partial_iteration_cleanup(in_dtype, buf_dtype, steps):
    """
    Checks for reference counting leaks during cleanup.  Using explicit
    reference counts lead to occasional false positives (at least in parallel
    test setups).  This test now should still test leaks correctly when
    run e.g. with pytest-valgrind or pytest-leaks
    """
    value = 2**30 + 1  # just a random value that Python won't intern
    arr = np.full(int(ncu.BUFSIZE * 2.5), value).astype(in_dtype)

    it = np.nditer(arr, op_dtypes=[np.dtype(buf_dtype)],
            flags=["buffered", "external_loop", "refs_ok"], casting="unsafe")
    for step in range(steps):
        # The iteration finishes in 3 steps, the first two are partial
        next(it)

    del it  # not necessary, but we test the cleanup

    # Repeat the test with `iternext`
    it = np.nditer(arr, op_dtypes=[np.dtype(buf_dtype)],
                   flags=["buffered", "external_loop", "refs_ok"], casting="unsafe")
    for step in range(steps):
        it.iternext()

    del it  # not necessary, but we test the cleanup

