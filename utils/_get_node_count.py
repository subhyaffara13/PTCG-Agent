
def _get_node_count(graph: Any) -> int:
    """Return the number of nodes currently in the graph."""
    _, num = _check_cuda_bindings(
        _cuda_runtime.cudaGraphGetNodes(  # pyrefly: ignore[missing-attribute]
            graph, numNodes=0
        )
    )
    return num

