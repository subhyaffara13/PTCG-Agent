
def test_iter_contig_flag_incorrect():
    # This case does the wrong thing...
    iterator = np.nditer(
        (np.ones((10, 10)).T, np.ones((1, 10))),
        flags=["external_loop", "reduce_ok", "buffered", "delay_bufalloc"],
        op_flags=[("readonly", "contig")] * 2)

    with iterator:
        iterator.reset()
        for a, b in iterator:
            # Remove a and b from locals (pytest may want to format them)
            a, b = a.strides, b.strides
            assert a == 8
            assert b == 8  # should be 8 but is 0 due to axis reorder

