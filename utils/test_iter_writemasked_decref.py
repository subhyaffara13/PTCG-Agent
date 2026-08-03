import sys

def test_iter_writemasked_decref():
    # force casting (to make it interesting) by using a structured dtype.
    arr = np.arange(10000).astype(">i,O")
    original = arr.copy()
    mask = np.random.randint(0, 2, size=10000).astype(bool)

    it = np.nditer([arr, mask], ['buffered', "refs_ok"],
                   [['readwrite', 'writemasked'],
                    ['readonly', 'arraymask']],
                   op_dtypes=["<i,O", "?"])
    singleton = object()
    if HAS_REFCOUNT:
        count = sys.getrefcount(singleton)
    for buf, mask_buf in it:
        buf[...] = (3, singleton)

    del buf, mask_buf, it   # delete everything to ensure correct cleanup

    if HAS_REFCOUNT:
        # The buffer would have included additional items, they must be
        # cleared correctly:
        assert sys.getrefcount(singleton) - count == np.count_nonzero(mask)

    assert_array_equal(arr[~mask], original[~mask])
    assert (arr[mask] == np.array((3, singleton), arr.dtype)).all()
    del arr

    if HAS_REFCOUNT:
        assert sys.getrefcount(singleton) == count

