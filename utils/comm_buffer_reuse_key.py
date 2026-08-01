
def comm_buffer_reuse_key(node: BufferLike) -> CommBufferReuseKey:
    # Comm buffers can only be reused by other comm buffers with the same (device, dtype, size, comm_buffer_type, group_name).
    storage_size = V.graph.get_allocation_storage_size(node)
    layout = node.get_output_spec()
    assert isinstance(layout, ir.CommBufferLayout)
    return (
        node.get_device_or_error(),
        node.get_dtype(),
        sympy_str(V.graph.sizevars.simplify(storage_size)),
        layout.comm_buffer_type,
        layout.group_name,
    )

