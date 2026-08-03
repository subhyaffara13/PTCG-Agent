import sys

def test_ufunc_out_casterrors():
    # Tests that casting errors are correctly reported and buffers are
    # cleared.
    # The following array can be added to itself as an object array, but
    # the result cannot be cast to an integer output:
    value = 123  # relies on python cache (leak-check will still find it)
    arr = np.array([value] * int(ncu.BUFSIZE * 1.5) +
                   ["string"] +
                   [value] * int(1.5 * ncu.BUFSIZE), dtype=object)
    out = np.ones(len(arr), dtype=np.intp)

    count = sys.getrefcount(value)
    with pytest.raises(ValueError):
        # Output casting failure:
        np.add(arr, arr, out=out, casting="unsafe")

    assert count == sys.getrefcount(value)
    # output is unchanged after the error, this shows that the iteration
    # was aborted (this is not necessarily defined behaviour)
    assert out[-1] == 1

    with pytest.raises(ValueError):
        # Input casting failure:
        np.add(arr, arr, out=out, dtype=np.intp, casting="unsafe")

    assert count == sys.getrefcount(value)
    # output is unchanged after the error, this shows that the iteration
    # was aborted (this is not necessarily defined behaviour)
    assert out[-1] == 1

