
def populate_stream_timeline(
    stream_to_timeline: dict[int | None, IndexedDict[Node, float]],
    graph: Graph,
    stream_index: int | None,
) -> IndexedDict[Node, float]:
    if stream_index not in stream_to_timeline:
        stream_to_timeline[stream_index] = IndexedDict()
        total_time = 0.0
        for node in graph.nodes:
            # mlazos: not sure if we should include forward here too but don't think it matters
            if (
                node.op == "call_function"
                and is_bwd_node(node)
                and get_stream(node) == stream_index
            ):
                total_time += get_roofline_estimate(node)
                stream_to_timeline[stream_index][node] = (
                    total_time  # NB: total time includes the node's runtime
                )

    return stream_to_timeline[stream_index]

