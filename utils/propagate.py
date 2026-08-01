
def propagate(amplifier_node: Node) -> None:
    log.debug("amplifier_node is %s", amplifier_node.format_node())
    # Chunk the batch dimension (dim 0) of the amplifier_node
    graph = amplifier_node.graph

    fwd_filter = can_reach_amplified_node(graph, amplifier_node, True)
    bwd_filter = can_reach_amplified_node(graph, amplifier_node, False)

    log.debug("fwd_filter %s", fwd_filter)
    log.debug("bwd_filter %s", bwd_filter)

    assert len(get_nodes_with_chunking_meta(graph)) == 0, (
        "Expect no nodes with chunking meta yet"
    )

    set_chunking_meta(amplifier_node, chunk_dim=0)

    queue: Queue[Node] = Queue()
    _enqueue(queue, amplifier_node)

    while not queue.empty():
        propagate_single_node(queue, fwd_filter, bwd_filter, queue.get())

    nodes_with_chunking_meta = get_nodes_with_chunking_meta(graph)
    propagate_scale_by(nodes_with_chunking_meta)

    if log.isEnabledFor(logging.DEBUG):
        print("All nodes with chunking metadata set:")
        for node in nodes_with_chunking_meta:
            format_node_with_chunking_meta(node)

