
def test_iter_contig_flag_reduce_error(read_or_readwrite):
    # Test that a non-contiguous operand is rejected without buffering.
    # NOTE: This is true even for a reduction, where we return a 0-stride
    #       below!
    with pytest.raises(TypeError, match="Iterator operand required buffering"):
        it = np.nditer(
            (np.zeros(()),), flags=["external_loop", "reduce_ok"],
            op_flags=[(read_or_readwrite, "contig"),], itershape=(10,))

