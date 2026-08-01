
def test_iter_contig_flag_single_operand_strides(arr):
    """
    Tests the strides with the contig flag for both broadcast and non-broadcast
    operands in 3 cases where the logic is needed:
    1. When everything has a zero stride, the broadcast op needs to repeated
    2. When the reduce axis is the last axis (first to iterate).
    3. When the reduce axis is the first axis (last to iterate).

    NOTE: The semantics of the cast flag are not clearly defined when
          it comes to reduction.  It is unclear that there are any users.
    """
    first_op = np.ones((10, 10))
    broadcast_op = arr()
    red_op = arr()
    # Add a first operand to ensure no axis-reordering and the result shape.
    iterator = np.nditer(
        (first_op, broadcast_op, red_op),
        flags=["external_loop", "reduce_ok", "buffered", "delay_bufalloc"],
        op_flags=[("readonly", "contig")] * 2 + [("readwrite", "contig")])

    with iterator:
        iterator.reset()
        for f, b, r in iterator:
            # The first operand is contigouos, we should have a view
            assert np.shares_memory(f, first_op)
            # Although broadcast, the second op always has a contiguous stride
            assert b.strides[0] == 8
            assert not np.shares_memory(b, broadcast_op)
            # The reduction has a contiguous stride or a 0 stride
            if red_op.ndim == 0 or red_op.shape[-1] == 1:
                assert r.strides[0] == 0
            else:
                # The stride is 8, although it was not originally:
                assert r.strides[0] == 8
            # If the reduce stride is 0, buffering makes no difference, but we
            # do it anyway right now:
            assert not np.shares_memory(r, red_op)

