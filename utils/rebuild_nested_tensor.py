
def rebuild_nested_tensor(
    rebuild_buffer_func,
    rebuild_buffer_args,
    rebuild_sizes_func,
    rebuild_sizes_args,
    rebuild_strides_func,
    rebuild_strides_args,
    rebuild_offsets_func,
    rebuild_offsets_args,
):
    buffer = rebuild_buffer_func(*rebuild_buffer_args)
    sizes = rebuild_sizes_func(*rebuild_sizes_args)
    strides = rebuild_strides_func(*rebuild_strides_args)
    offsets = rebuild_offsets_func(*rebuild_offsets_args)
    return torch._nested_view_from_buffer_copy(buffer, sizes, strides, offsets)

