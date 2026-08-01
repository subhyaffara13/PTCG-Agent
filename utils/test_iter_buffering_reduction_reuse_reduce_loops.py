
def test_iter_buffering_reduction_reuse_reduce_loops():
    # There was a bug triggering reuse of the reduce loop inappropriately,
    # which caused processing to happen in unnecessarily small chunks
    # and overran the buffer.

    a = np.zeros((2, 7))
    b = np.zeros((1, 7))
    it = np.nditer([a, b], flags=['reduce_ok', 'external_loop', 'buffered'],
                    op_flags=[['readonly'], ['readwrite']],
                    buffersize=5)

    with it:
        bufsizes = [x.shape[0] for x, y in it]
    assert_equal(bufsizes, [5, 2, 5, 2])
    assert_equal(sum(bufsizes), a.size)

