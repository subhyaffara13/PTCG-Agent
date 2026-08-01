
def _rebuild_nested_tensor(buffer, sizes, strides, storage_offsets):
    return torch._nested_view_from_buffer(buffer, sizes, strides, storage_offsets)

