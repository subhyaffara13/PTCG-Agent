
def _reduce_scatter_tensor_coalesced_native_meta(
    inputs, reduce_op, group_size, group_name
):
    return [
        _reduce_scatter_tensor_native_meta(inp, reduce_op, group_size, group_name)
        for inp in inputs
    ]

