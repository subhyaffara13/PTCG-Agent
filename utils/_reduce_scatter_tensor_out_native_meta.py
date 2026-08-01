
def _reduce_scatter_tensor_out_native_meta(
    inp, reduce_op, group_size, group_name, *, out
):
    shape = list(inp.size())
    shape[0] //= group_size
    return inp.new_empty(shape)

