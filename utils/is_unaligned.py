
def is_unaligned(node: IRNode) -> bool:
    if isinstance(node, (TensorBox, StorageBox)):
        return is_unaligned(node.data)

    if isinstance(node, ReinterpretView):
        layout = node.layout
        has_unaligned_layout = not V.graph.sizevars.statically_known_multiple_of(
            layout.offset * get_dtype_size(layout.dtype), GPU_ALIGN_BYTES
        )
        return is_unaligned(node.data) or has_unaligned_layout

    if isinstance(node, Buffer):
        return node.get_name() in V.graph.unaligned_buffers

    # assume to be aligned otherwise
    return False

