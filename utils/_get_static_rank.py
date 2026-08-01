
def _get_static_rank(tensor_name: str, graph_path: list[GraphProto]) -> int | None:
    """Return the static rank of a tensor if its shape is known, else None.

    Searches graph inputs, value_info, and outputs in the graph stack (inner-most
    graph first).  A known shape requires ``HasField('shape')`` to be true on the
    tensor_type; the rank is then ``len(shape.dim)``.  Individual dim sizes may
    still be symbolic — only the rank (dimension count) matters here.
    """
    for gid in range(len(graph_path) - 1, -1, -1):
        graph = graph_path[gid]
        for vi in list(graph.input) + list(graph.value_info) + list(graph.output):
            if vi.name == tensor_name:
                tt = vi.type.tensor_type
                if tt.HasField("shape"):
                    return len(tt.shape.dim)
                return None
    return None

