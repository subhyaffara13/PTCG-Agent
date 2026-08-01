
def can_match_buffer_size(input_buf: BufferLike, output_buf: BufferLike):
    # Return True if input_buf can be re-inplaced for output_buf.
    # This differs from `buffer_reuse_key` for general buffer reuse.
    if input_buf.get_device_or_error() != output_buf.get_device_or_error():
        return False

    if input_buf.get_dtype() != output_buf.get_dtype():
        return False

    input_size = V.graph.sizevars.simplify(
        V.graph.get_allocation_storage_size(input_buf)
    )
    output_size = V.graph.sizevars.simplify(
        V.graph.get_allocation_storage_size(output_buf)
    )

    if (
        # NB: this is symbolic so that we don't try to reuse a buffer
        # for s0 for s1, just because they happen to share the same
        # size hint
        sympy_str(input_size) == sympy_str(output_size)
    ) or (
        # statically known that 0.95 * input_size <= output_size <= input_size
        V.graph.sizevars.statically_known_geq(output_size, 0.95 * input_size)
        and V.graph.sizevars.statically_known_leq(output_size, input_size)
    ):
        return True

    return False

