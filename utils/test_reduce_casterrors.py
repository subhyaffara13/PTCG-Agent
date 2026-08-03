import sys

def test_reduce_casterrors(offset):
    # Test reporting of casting errors in reductions, we test various
    # offsets to where the casting error will occur, since these may occur
    # at different places during the reduction procedure. For example
    # the first item may be special.
    value = 123  # relies on python cache (leak-check will still find it)
    arr = np.array([value] * offset +
                   ["string"] +
                   [value] * int(1.5 * ncu.BUFSIZE), dtype=object)
    out = np.array(-1, dtype=np.intp)

    count = sys.getrefcount(value)
    with pytest.raises(ValueError, match="invalid literal"):
        # This is an unsafe cast, but we currently always allow that.
        # Note that the double loop is picked, but the cast fails.
        # `initial=None` disables the use of an identity here to test failures
        # while copying the first values path (not used when identity exists).
        np.add.reduce(arr, dtype=np.intp, out=out, initial=None)
    assert count == sys.getrefcount(value)
    # If an error occurred during casting, the operation is done at most until
    # the error occurs (the result of which would be `value * offset`) and -1
    # if the error happened immediately.
    # This does not define behaviour, the output is invalid and thus undefined
    assert out[()] < value * offset

