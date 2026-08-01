
def test_large_string_cast():
    very_large = np.iinfo(np.intc).max // 4
    # Could be nice to test very large path, but it makes too many huge
    # allocations right now (need non-legacy cast loops for this).
    # a = np.array([], dtype=np.dtype(("S", very_large)))
    # assert a.astype("U").dtype.itemsize == very_large * 4

    a = np.array([], dtype=np.dtype(("S", very_large + 1)))
    # It is not perfect but OK if this raises a MemoryError during setup
    # (this happens due clunky code and/or buffer setup.)
    with pytest.raises((TypeError, MemoryError)):
        a.astype("U")

