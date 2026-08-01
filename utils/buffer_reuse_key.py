
def buffer_reuse_key(node: BufferLike) -> ReuseKey:
    storage_size = V.graph.get_allocation_storage_size(node)
    alignment = node.get_name() not in V.graph.unaligned_buffers
    stream = V.graph.scheduler.get_buf_stream(node.get_name())
    return (
        node.get_device_or_error(),
        node.get_dtype(),
        # NB: this is symbolic so that we don't try to reuse a buffer
        # for s0 for s1, just because they happen to share the same
        # size hint
        sympy_str(V.graph.sizevars.simplify(storage_size)),
        alignment,
        stream,
    )

