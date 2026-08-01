
def _initialize_memory_tracking(snodes, graph_inputs, graph_outputs):
    """Initialize memory tracking data structures"""
    name_to_freeable_input_buf = get_freeable_input_buf(snodes, graph_inputs)
    peak_memory, snodes_curr_memory, snodes_allocfree, buf_to_snode_last_use = (
        estimate_peak_memory_allocfree(
            snodes, name_to_freeable_input_buf, graph_outputs
        )
    )
    _curr_memory = dict(zip(snodes, snodes_curr_memory))
    # pyrefly: ignore [unsupported-operation]
    _curr_memory[None] = (0, 0)

    # Build candidate buffer map for optimization
    candidate_buffer_map = _build_candidate_buffer_map(buf_to_snode_last_use)

    return (
        peak_memory,
        _curr_memory,
        snodes_allocfree,
        buf_to_snode_last_use,
        name_to_freeable_input_buf,
        candidate_buffer_map,
    )

