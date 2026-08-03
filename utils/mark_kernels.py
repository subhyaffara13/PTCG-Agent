from typing import Any

def mark_kernels(annotation: str | dict[str, Any]):
    """Context manager that records node index ranges for later annotation.

    During capture, calls ``cudaGraphGetNodes`` to count graph nodes before
    and after the scope.  Nodes at indices ``[before, after)`` were added
    inside the scope.  After capture, ``resolve_pending_annotations``
    enumerates all nodes and annotates kernel/memcpy nodes in those ranges.

    Must be called inside an active ``torch.cuda.graph()`` capture.  If the
    current stream is not capturing, or if ``cudaGraphNodeGetToolsId`` is not
    available, the context manager is a no-op.

    Args:
        annotation: Arbitrary object appended to the annotation list for
            every kernel/memcpy node whose index falls within this scope.
    """
    if not _annotations_enabled or _is_tools_id_unavailable():
        yield
        return

    if isinstance(annotation, str):
        annotation = {"str": annotation}

    stream = _cuda_runtime.cudaStream_t(  # pyrefly: ignore[missing-attribute]
        init_value=torch.cuda.current_stream().cuda_stream
    )
    graph = _get_capture_graph(stream)
    if graph is None:
        yield
        return

    global _capture_graph
    _capture_graph = graph

    start_count = _get_node_count(graph)

    yield

    end_count = _get_node_count(graph)

    if end_count > start_count:
        _pending_scopes.append((annotation, start_count, end_count))

