
def _build_candidate_buffer_map(
    buf_to_snode_last_use: dict,
) -> dict[BaseSchedulerNode, OrderedSet]:
    """
    Build inverted index: node -> set of buffers where node appears in successors.

    This optimization reduces buffer iteration from O(total_buffers) to O(buffers_per_node).
    Since buffer successors are immutable during reordering, this map doesn't need updates.

    Returns:
        dict mapping each node to the set of buffers that have this node in their successors
    """
    node_to_candidate_bufs: dict[BaseSchedulerNode, OrderedSet] = defaultdict(
        OrderedSet
    )

    for buf in buf_to_snode_last_use:
        # Add to every successor node's buffer set
        for succ_node in buf.mpi_buffer.succ_nodes:
            node_to_candidate_bufs[succ_node].add(buf)

    return dict(node_to_candidate_bufs)

