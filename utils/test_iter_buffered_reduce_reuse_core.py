
def test_iter_buffered_reduce_reuse_core():
    # NumPy re-uses buffers for broadcast operands (as of writing when reading).
    # Test this even if the offset is manually set at some point during
    # the iteration.  (not a particularly tricky path)
    arr = np.empty((1, 6, 4, 1)).reshape(1, 6, 4, 1)[:, ::3, ::2, :]
    arr[...] = np.arange(arr.size).reshape(arr.shape)
    # First and last dimension are broadcast dimensions.
    arr = np.broadcast_to(arr, (100, 2, 2, 2))

    flags = ['buffered', 'reduce_ok', 'refs_ok', 'multi_index']
    op_flags = [('readonly',)]

    buffersize = 100  # small enough to not fit the whole array
    it = np.nditer(arr, flags=flags, op_flags=op_flags, buffersize=100)

    # Iterate a bit (this will cause buffering internally)
    expected = [next(it) for i in range(11)]
    # Now, manually advance to inside the core (the +1)
    it.iterindex = 10 * (2 * 2 * 2) + 1
    result = [next(it) for i in range(10)]

    assert expected[1:] == result

