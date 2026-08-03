import sys

def test_reduction_no_reference_leak():
    # Test that the generic reduction does not leak references.
    # gh-29358
    arr = np.array([1, 2, 3], dtype=np.int32)
    count = sys.getrefcount(arr)

    np.add.reduce(arr, dtype=np.int32, initial=0)
    assert count == sys.getrefcount(arr)

    np.add.accumulate(arr, dtype=np.int32)
    assert count == sys.getrefcount(arr)

    np.add.reduceat(arr, [0, 1], dtype=np.int32)
    assert count == sys.getrefcount(arr)

    # with `out=` the reference count is not changed
    out = np.empty((), dtype=np.int32)
    out_count = sys.getrefcount(out)

    np.add.reduce(arr, dtype=np.int32, out=out, initial=0)
    assert count == sys.getrefcount(arr)
    assert out_count == sys.getrefcount(out)

    out = np.empty(arr.shape, dtype=np.int32)
    out_count = sys.getrefcount(out)

    np.add.accumulate(arr, dtype=np.int32, out=out)
    assert count == sys.getrefcount(arr)
    assert out_count == sys.getrefcount(out)

    out = np.empty((2,), dtype=np.int32)
    out_count = sys.getrefcount(out)

    np.add.reduceat(arr, [0, 1], dtype=np.int32, out=out)
    assert count == sys.getrefcount(arr)
    assert out_count == sys.getrefcount(out)

